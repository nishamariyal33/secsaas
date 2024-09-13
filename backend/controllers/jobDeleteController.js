const axios=require('axios');
const handleDeleteJob = async (req, res) => {
    axios.delete(`http://localhost:8005/deleteJob/${req.body.jobId}`,
        {
            headers: { 'Content-Type': 'application/json' ,
            'Authorization':req.headers.authorization},
        }
    ).then((response)=>{
        res.status(200).send({
            data:response.data,
        message:"Scan created successfully"});
    }).catch((error)=>{
        console.log('Error in handleDeleteJob ');
    });
    // TODO: remove console.logs before deployment
        
}

module.exports = { handleDeleteJob };