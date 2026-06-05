const express = require('express')

const {
  getTaskById,
  createTask,
  deleteTaskById,
  editTaskById,
  getTaskByUserId
} = require('../models/task')

const router = express.Router()

router.get('/tasks/:id', (req, res, next) => {
  const id = Number(req.params.id)
  return getTaskById(id)
    .then((task) => res.json(task))
    .catch((err) => {
      res.status(500).json({ message: err.message })
    })
})

router.get('/tasks/users/:id', (req, res, next) => {
  // Write your code here
})

router.post('/tasks', (req, res, next) => {
  const {
    user_id,
    name,
    description,
    creation_date,
    due_date,
    due_time,
    priority_level,
    status,
  } = req.body

  
})

router.delete('/tasks/:id', (req, res, next) => {
  // Write your code here
})

router.put('/tasks/:id', (req, res, next) => {
 // Write your code here
})


module.exports = router
