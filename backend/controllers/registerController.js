const User = require('../model/User');
const bcrypt = require('bcrypt');
const axios=require('axios');
const handleNewUser = async (req, res) => {
    axios.post("http://localhost:8005/register",
        req.body,
        {
            headers: { 'Content-Type': 'application/json' },
        }
    ).then((response)=>{
        res.status(200).send(response.data.tenantId);
    }).catch((error)=>{
        console.log('Error in handleNewUser ',error);
    });
    // TODO: remove console.logs before deployment
        
}

module.exports = { handleNewUser };