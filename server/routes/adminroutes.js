import express from 'express';
import bcrypt from 'bcryptjs';
import User from '../models/user.js';
import Order from '../models/order.js';
import { authenticateJWT, requireRole } from '../middleware/authenticateJWT.js';

const router = express.Router();

router.use(authenticateJWT, requireRole('admin'));

// Listar todos los usuarios
router.get('/users', async (req, res) => {
  try {
    const users = await User.find().select('-password');
    res.json(users);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Crear usuario desde zona admin
router.post('/users', async (req, res) => {
  try {
    const { username, password, role = 'user' } = req.body;

    if (!username || !password) {
      return res.status(400).json({ message: 'username y password son obligatorios' });
    }

    const exists = await User.findOne({ username });
    if (exists) {
      return res.status(409).json({ message: 'El usuario ya existe' });
    }

    const hashed = await bcrypt.hash(password, 10);
    const user = await User.create({ username, password: hashed, role });

    res.status(201).json({
      _id: user._id,
      username: user.username,
      role: user.role,
      orders: user.orders,
    });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Actualizar rol de usuario
router.put('/users/:id', async (req, res) => {
  try {
    const { role } = req.body;
    if (!['admin', 'user'].includes(role)) {
      return res.status(400).json({ message: 'Rol inválido' });
    }

    const updated = await User.findByIdAndUpdate(
      req.params.id,
      { role },
      { new: true }
    ).select('-password');

    if (!updated) {
      return res.status(404).json({ message: 'Usuario no encontrado' });
    }

    res.json(updated);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Eliminar usuario
router.delete('/users/:id', async (req, res) => {
  try {
    if (String(req.user.id) === String(req.params.id)) {
      return res.status(400).json({ message: 'No puedes eliminarte a ti mismo' });
    }

    const deleted = await User.findByIdAndDelete(req.params.id);
    if (!deleted) {
      return res.status(404).json({ message: 'Usuario no encontrado' });
    }

    res.json({ message: 'Usuario eliminado' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Listar todos los pedidos
router.get('/orders', async (req, res) => {
  try {
    const orders = await Order.find().populate('user').populate('items.product');
    res.json(orders);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Filtrar pedidos por estado
router.get('/orders/:status', async (req, res) => {
  try {
    const orders = await Order.find({ status: req.params.status }).populate('user').populate('items.product');
    res.json(orders);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

export default router;