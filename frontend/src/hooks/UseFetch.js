import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

export default function useFetch(url, { method, headers, body } = {}) {
    const [data, setData] = useState();
    const [errorStatus, setErrorStatus] = useState();

    const navigate = useNavigate();
    const location = useLocation();
   async function request() {
        fetch("http://localhost:4000/getScanJobs", {
            method: "GET",
            headers: headers
        })
            .then((response) => {
                if (response.status === 401) {
                    navigate('/login', {
                        state: {
                            previousUrl: location.pathname,
                        },
                    });
                }
                if (!response.ok) {
                    throw response.status;
                }
                return response.json();
            })
            .then((data) => {
                console.log("dataaaaaaa ",data)
                data.customers.length=10;
                console.log("zzzzzz",data);
                setData(data);
            })
            .catch((e) => {
                setErrorStatus(e);
            });
    }

    function appendData(newData) {
        console.log("zzzzzz ",newData)
        fetch("http://localhost:4000/job", {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(newData),
        })
            .then((response) => {
                console.log("aaaaa ",response)
                if (response.status === 401) {
                    navigate('/login', {
                        state: {
                            previousUrl: location.pathname,
                        },
                    });
                }

                if (!response.ok) {
                    throw response.status;
                }

                return response.json();
            })
            .then((d) => {
                console.log("xxsssss ",data)
                const submitted = Object.values(d)[0];
                console.log("xxsssss123 ",submitted)
                const newState = { ...data };
                console.log("xxbbbbb ",newState)
                newState.customers.unshift(submitted);
                console.log("qxxxxxx ",newState)
                setData(newState); //new object, it's seen as a state change
            })
            .catch((e) => {
                console.log(e);
                setErrorStatus(e);
            });
    }

    function removeData(jobId, index) {
        fetch(`http://localhost:4000/deleteJob`, {
            method: 'DELETE',
            headers: headers,
            body:JSON.stringify({jobId})
        })
            .then((response) => {
                if (response.status === 401) {
                    navigate('/login', {
                        state: {
                            previousUrl: location.pathname,
                        },
                    });
                }

                if (!response.ok) {
                    throw response.status;
                }

                return response.json();
            })
            .then((d) => {
                // let currindex=-1;
                // console.log("xxsssss ",data)
                // const submitted = Object.values(d)[0];
                // console.log("fgvdsfdsvcsdf ",submitted)
                const newState = { ...data };
                // console.log("indexxxxxx ",currindex, index)
                newState.customers.splice(index, 1);
                setData(newState); //new object, it's seen as a state change
            })
            .catch((e) => {
                console.log(e);
                setErrorStatus(e);
            });
    }


    return { request, appendData, data, errorStatus,removeData };
}
