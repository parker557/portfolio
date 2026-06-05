//const db = require('./index')
//const knex = require('./index')

const knex = require('./index')
const createUser = (user_name, first_name, last_name, email, password_hash) => {
	
    return knex('users').where('email', email)  
    .orWhere('user_name', user_name)  
    .first()  
    .then(existingUser => {  
		if (existingUser) {  
			console.log("User already exists"); 
			return null;
		} 
		else {  
		  return knex('users').insert({  
			user_name: user_name,  
			first_name: first_name,  
			last_name: last_name,  
			email: email,  
			password_hash: password_hash  
		  })
		  .returning('id')
		  .then(rows => {
			return rows[0];
		  });
		 
		}  
  })
 
  
}

const getUserByEmail = (email) => {
  return knex("users").where({email: email}).first();
  
}

const getUserById = (id) => {  
  return knex("users").where({id: id}).first();
}

const updateUserPassById = (id, password_hash) => {  
  return knex('users').where({id: id}).update({password_hash: password_hash});
}



module.exports = {
  createUser,
  getUserByEmail,
  getUserById,
  updateUserPassById
}
