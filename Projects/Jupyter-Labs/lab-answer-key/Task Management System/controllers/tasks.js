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
  const id = Number(req.params.id)
  return getTaskByUserId(id)
    .then((data) => {
      //console.log(data)
      res.json(data)
    })
    .catch((err) => {
      res.status(500).json({ message: err.message })
    })
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

  return createTask(
	user_id,
    name,
    description,
    creation_date,
    due_date,
    due_time,
    priority_level,
    status
  )
    .then((task) => {
      res.status(201).json({
        id: task.id,
        message: 'Task created successfully',
      })
    })
    .catch((err) => {
      res.status(500).json({ message: err.message })
    })
})

router.delete('/tasks/:id', (req, res, next) => {
  const id = Number(req.params.id)
  return deleteTaskById(id)
    .then((task) => {
      if (task.rowCount === 0) {
        const error = new Error(`Task with ID ${id} not found`)
        error.status = 404
        throw error
      } else {
        res.status(204)
      }
    })
    .catch((err) => {
      res.status(500).json({ message: err.message })
    })
})

router.put('/tasks/:id', (req, res, next) => {
  const id = Number(req.params.id)
  const { name, description, due_date, due_time, priority_level, status } = req.body

  if (!name && !description && !due_date && !due_time && !priority_level && !status) {
    const error = new Error('No value updated for task details.')
    error.status = 400
    throw error
  }
  return editTaskById(name, description, due_date, due_time, priority_level, status, id)
    .then((taskDetails) => {
      res.sendStatus(taskDetails.rowCount === 0 ? 404 : 200)
    })
    .catch((err) => {
      res.status(500).json({ message: err.message })
    })
})


module.exports = router
