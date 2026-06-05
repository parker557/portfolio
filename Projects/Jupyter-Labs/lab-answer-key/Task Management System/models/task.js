const knex = require('./index')


const getTaskById = (id) => {
  return knex("tasks").where({id: id});
}

const getTaskByUserId = (id) => {
  return knex("tasks").where({user_id: id});
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
  
   return knex('tasks').insert({user_id: user_id, name: name, description:description, creation_date:creation_date, due_date:due_date, due_time:due_time, priority_level:priority_level, status: status});
  
  
}

const deleteTaskById = (id) => {
	
  return knex("tasks").where({id: id}).del();
}

const editTaskById = (name, description, due_date, due_time, priority_level, status, id) => {

  return knex('tasks').where({id: 1}).update({name: name, description:description, due_date:due_date, due_time:due_time, priority_level:priority_level, status: status});
}


module.exports = {
  getTaskById,
  deleteTaskById,
  createTask,
  editTaskById,
  getTaskByUserId
}
