const axios=require('axios');
const handleNewJob = async (req, res) => {
    axios.post("http://localhost:8005/job",
        req.body,
        {
            headers: { 'Content-Type': 'application/json' ,
            'Authorization':req.headers.authorization},
        }
    ).then((response)=>{
        res.status(200).send({
            data:response.data,
        message:"Scan created successfully"});
    }).catch((error)=>{
        console.log('Error in handleNewJob ',error);
    });
    // TODO: remove console.logs before deployment
        
}

module.exports = { handleNewJob };