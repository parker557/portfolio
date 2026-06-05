//Contains all API route definations for users
const axios = require('axios')
const express = require('express')
const bcrypt = require('bcrypt')
const {
  createUser,
  getUserById,
  updateUserPassById,
  getUserByEmail
} = require('../models/user')

const router = express.Router()
const generateHash = (password) => {
  if (!password) {
    throw new Error()
  }
  return bcrypt.hashSync(password, bcrypt.genSaltSync(10), null)
}

const comparePassword = (password, password_hash) => {
  if (typeof password !== 'string' || !password) {
    throw new Error()
  }
  const result = bcrypt.compareSync(password, password_hash)
  return result
}

router.post('/users', async (req, res, next) => {
  try {
	  const { username, firstname, lastname, email, password1, password2 } = Object.entries(
		req.body
	  ).reduce((obj, [key, value]) => {
		obj[key] = value.trim()
		return obj
	  }, {})

	  if (!username || !firstname || !lastname || !email || !password1 || !password2) {
		const customError = new Error('The name, email or password is missing.')
		customError.status = 400
		return next(customError)
	  }
	  if (password1 !== password2) {
		const customError = new Error('The passwords do not match. Please try again')
		customError.status = 400
		return next(customError)
	  }
	  if (password1.length < 8) {
		const customError = new Error('The password is too short. It must be 8 characters long.')
		customError.status = 400
		return next(customError)
	  }
	  const specialChars = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/
	  if (
		!/\d/.test(password1) ||
		!/[A-Z]/.test(password1) ||
		!/[a-z]/.test(password1) ||
		!specialChars.test(password1)
	  ) {
		const customError = new Error(
		  'The password must contain a combination of uppercase letters, lowercase letters, numbers and symbols.'
		)
		customError.status = 400
		return next(customError)
	  }

	  const passwordHash = generateHash(password1)

	  const userRes = await createUser(username, firstname, lastname, email, passwordHash)
	  if (!userRes) {
		const customError = new Error(
		  'The email address or username is already used by an existing user. Try Loggin in.'
		)
		customError.status = 409
		return next(customError)
	  }
	  const user = {
		id: userRes.id,
		user_name: username,
		first_name: firstname,
		last_name: lastname,
		email,
	  }

	  req.session.user = user
	  return res.status(200).json({ user })
  } catch (err) {
    next(err)
  }
})

router.put('/users/:id', async (req, res, next) => {
 // Task: Update user information based on user id 	
 // Write your code here
})

router.get('/users/:email', async (req, res, next) => {
  // Task: User login： Obtain user information based on email
 // Write your code here
})




module.exports = { router, generateHash, comparePassword }
