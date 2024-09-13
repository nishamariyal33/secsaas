const axios = require('axios');
const handleCurrentUser = async (req, res) => {
    axios.get("http://localhost:8005/currentUser",
        {
            headers: {
                'Authorization': req.headers.authorization,
            },
        }
    ).then((response) => {
        res.status(200).send({
            data: response.data,
            message: "Scan List retrieved successfully"
        });
    }).catch((error) => {
        console.log('Error in handleCurrentUser ');
    });
    // TODO: remove console.logs before deployment

}

module.exports = { handleCurrentUser };