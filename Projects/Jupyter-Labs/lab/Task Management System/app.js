require('dotenv').config()

const express = require('express')
const session = require('express-session')
const pgSession = require('connect-pg-simple')(session)


const tasksRouter = require('./controllers/tasks')
const { router } = require('./controllers/users')
const usersRouter = router
const sessionRouter = require('./controllers/sessions')

// above two lines will be for the routers to each of our controllers .js files

//imports middleware
const httpLoggerMiddleware = require('./middlewares/httpLogger')
const errorHandlingMiddleware = require('./middlewares/errorHandling')

//const {db} = require('./models/')



const app = express()
const port = process.env.HTTP_PORT || 3000

app.use(express.static('client'))
app.use(express.json())
app.use(
  session({
    secret: "your secret key",
    resave: false,
    saveUninitialized: false
  })
)

// code to app.use routers and any middleware
app.use(httpLoggerMiddleware)
app.use(
  '/api',
  usersRouter,
  sessionRouter,
  tasksRouter
)
app.use(errorHandlingMiddleware)

app.listen(port, () => {
  console.log('Server started on port: ' + port)
})
