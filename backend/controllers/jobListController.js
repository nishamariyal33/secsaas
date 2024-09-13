const axios=require('axios');
const handleJobList = async (req, res) => {
    req.body["scanType"]="hostedscan"
    axios.get("http://localhost:8005/getScanJobs",
    {
        data:req.body,
            headers: {  
            'Authorization':req.headers.authorization,
            },
        }
    ).then((response)=>{
        res.status(200).send({
            customers:response.data.data,
        message:"Scan List retrieved successfully"});
    }).catch((error)=>{
        console.log('Error in handleJobList');
    });
    // TODO: remove console.logs before deployment
        
}

module.exports = { handleJobList };