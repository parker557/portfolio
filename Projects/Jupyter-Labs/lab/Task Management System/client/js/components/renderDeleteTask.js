import { renderTasks } from './renderTasks.js'
const renderDeleteTask = async (taskId, user) => {
  const confirmed = confirm('Are you sure you want to delete this task?')
  console.log(taskId)

  function deleteTask() {
    return axios
      .delete(`/api/tasks/${taskId}`)
      .then(async (res) => {
        console.log(res)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  async function renderNew() {
    document.querySelector('#main-content').innerHTML = ''
    renderTasks(user)
  }

  if (confirmed) {
    deleteTask().then(renderNew())
  }
}

export default renderDeleteTask
