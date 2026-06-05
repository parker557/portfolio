const knex = require('./index')


const getTaskById = (id) => {
  return knex("tasks").where({id: id});
}

const getTaskByUserId = (id) => {
  // Write your code here
}


const createTask = (
  user_id,
  name,
  description,
  creation_date,
  due_date,
  due_time,
  priority_level,
  status
) => {
  
  const values = [
    user_id,
    name,
    description,
    creation_date,
    due_date,
    due_time,
    priority_level,
    status,
  ]
  
  // Write your code here
  
  
}

const deleteTaskById = (id) => {
	
  // Write your code here
}

const editTaskById = (name, description, due_date, due_time, priority_level, status, id) => {

  // Write your code here
}


module.exports = {
  getTaskById,
  deleteTaskById,
  createTask,
  editTaskById,
  getTaskByUserId
}
