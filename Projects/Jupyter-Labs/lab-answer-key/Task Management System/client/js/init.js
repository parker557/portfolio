import renderHeader from './components/renderHeader.js'
import {renderTasks} from './components/renderTasks.js'

axios
  .get('/api/session')
  .then(({ data }) => {
    if ('user' in data) {
      renderHeader(data.user)
	  renderTasks(data.user)
    } else {
      window.location = '/entry.html'
    }
  })
  .catch((err) => console.error(err))
