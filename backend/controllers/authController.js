const User = require('../model/User');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const axios=require('axios');
const handleLogin = async (req, res) => {
    const { user, pwd } = req.body;
    const response = await axios.post(`http://localhost:8005/login?tenantId=${req.body.tenantId}`,
    { username:user, password:pwd },
    {
        headers: { 'Content-Type': 'application/json' },
    });
    if (response.status!=200) return res.sendStatus(401); //Unauthorized 
    // evaluate password 
  
        // Send authorization roles and access token to user
        res.status(200).send(response.data);
}

module.exports = { handleLogin };