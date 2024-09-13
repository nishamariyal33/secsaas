const axios=require('axios');
const fs=require('fs');
const filepath="/Users/kishorehari/Downloads/reports/report1.pdf"
const readFile=async(filePath)=>{
    return new Promise((resolve,reject)=>{
        resolve (fs.readFileSync(filePath));
    })
    
}
const handleJobResult = async (req, res) => {
    req.body["scanType"]="hostedscan"
    // axios.get("http://localhost:8005/getScanResult", {
    //     data:req.body,
    //         headers: {  
    //         'Authorization':req.headers.authorization,
    //         },
    //     },function(req, res) {
    //         console.log("sssssss ",__dir);
    //     res.download('/Users/kishorehari/Downloads/reports/report.pdf');
    //   });
    axios.get("http://localhost:8005/getScanResult",
    {
        data:req.body,
            headers: {  
            'Authorization':req.headers.authorization,
            },
            responseType: 'stream'
        }
    ).then(async(response)=>{
        await response.data.pipe(await fs.createWriteStream(filepath)); 
       await readFile(filepath).then((report)=>{
            console.log("saaaaa ",report.byteLength)
            res.status(200).send({data:report});
        })
    }).catch((error)=>{
        console.log('22222 ',error);
    });
    // TODO: remove console.logs before deployment
        
}

module.exports = { handleJobResult };