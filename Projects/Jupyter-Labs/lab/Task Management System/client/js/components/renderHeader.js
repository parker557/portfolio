import renderUserProfile from './renderUserProfile.js'


const renderHeader = (user) => {
  const header1 = document.getElementById('header-nav')

  const display = document.querySelector('.display-bg')
  if (display) {
    display.remove()
  }
  header1.innerHTML = `
    <nav class="navbar nav-1" style="background-color: #fbfded; border-bottom: solid 1px #F9D949">
        <div class="container-fluid">
            <a class="navbar-brand" href="#"><img id="logo-img" src="./images/tskr-high-resolution-logo-black-on-transparent-background.png" alt="logo"></a>
            <div class="nav-item dropdown px-5">
                <a class="nav-link dropdown-toggle name-display" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    ${user.user_name}
                </a>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item user-detail" href="#">View Details</a></li>
                    <li><a class="dropdown-item logout-btn" href="#">Logout</a></li>
                </ul>
            </div>
        </div>
    </nav>  `




  const logoutBtn = document.querySelector('.logout-btn')
  logoutBtn.addEventListener('click', () => {
    axios.delete('/api/session').then((res) => (window.location = '/entry.html'))
  })

  const userDetail = document.querySelector('.user-detail')
  userDetail.addEventListener('click', () => {
    axios.get('/api/session').then(({ data }) => {
      renderUserProfile(user)
    })
  })

}

export default renderHeader
