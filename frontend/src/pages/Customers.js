import { useEffect, useState, useContext } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { confirmAlert } from 'react-confirm-alert'; // Import
import 'react-confirm-alert/src/react-confirm-alert.css';
import AddCustomer from '../components/AddCustomer';
import DeleteCustomer from '../components/DeleteCustomer';
import { baseUrl } from '../shared';
import { LoginContext } from '../App';
import useFetch from '../hooks/UseFetch';

export default function Customers() {
    const [loggedIn, setLoggedIn] = useContext(LoginContext);
    // const [customers, setCustomers] = useState();
    const [show, setShow] = useState(false);
    const [showDelete, setShowDelete] = useState(false)
    function toggleShow() {
        setShow(!show);
    }

    function toogleDeleteShow() {
        setShowDelete(!showDelete)
    }

    const location = useLocation();
    const navigate = useNavigate();

    const url = baseUrl + 'api/customers/';
    const {
        request,
        appendData,
        data: { customers } = {},
        errorStatus,
        removeData

    } = useFetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            Authorization: localStorage.getItem('access'),
        },
    });

    useEffect(() => {
        request();
    }, []);

    //useEffect(() => {
    //    console.log(request, appendData, customers, errorStatus);
    //});

    function handleClick(job_id) {
        console.log('wwwww ', job_id)
        fetch(`http://localhost:4000/scan/getScanResult`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'responseType': 'blob',
                Authorization: localStorage.getItem('access'),

            },
            body: JSON.stringify({ job_id, file_format: "pdf" })
        })
            .then(async (res) => {
                const response = await res.json();
                console.log("zzzzz", response.data)
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'report.pdf'); //or any other extension
                document.body.appendChild(link);
                link.click();

            }).catch((error) => {
                console.log("errorrrr ", error);
            })


    };

    function newScan(targetUrl, scanType, type) {
        appendData({ targetUrl: targetUrl, scanType: scanType, type });

        if (!errorStatus) {
            toggleShow();
        }
    }

    function submit (jobId, index){

        confirmAlert({
          title: 'Confirm to submit',
          message: 'Are you sure to do this.',
          buttons: [
            {
              label: 'Yes',
              onClick: () => deleteScan(jobId, index)
            },
            {
              label: 'No',
              //onClick: () => alert('Click No')
            }
          ]
        });
    }

    function deleteScan(jobId, index) {
        removeData(jobId, index);

        if (!errorStatus) {
            toogleDeleteShow();
        }
    }

    return (
        <>
            <AddCustomer
                newScan={newScan}
                show={show}
                toggleShow={toggleShow}
            />
            <h1>Here are the list of scans created:</h1>
            <div class="flex flex-col">
                <div class="overflow-x-auto sm:-mx-6 lg:-mx-8">
                    <div class="py-4 inline-block min-w-full sm:px-6 lg:px-8">
                        <div class="overflow-hidden">
                            <table class="min-w-full text-center">
                                <thead class="border-b bg-gray-800">
                                    <tr>
                                        <th scope="col" class="text-sm font-medium text-white px-6 py-4">
                                            #
                                        </th>
                                        <th scope="col" class="text-sm font-medium text-white px-6 py-4">
                                            Target
                                        </th>
                                        <th scope="col" class="text-sm font-medium text-white px-6 py-4">
                                            State
                                        </th>
                                        <th scope="col" class="text-sm font-medium text-white px-6 py-4">
                                            Scan
                                        </th>
                                        <th scope="col" class="text-sm font-medium text-white px-6 py-4">
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white border-b">
                                    {customers ? customers.map((customer, index) => (
                                        <tr key={customer.jobId}>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{index + 1}</td>
                                            <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                                                {customer.requested_targets[0].target}
                                            </td>
                                            <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                                                {customer.state}
                                            </td>
                                            <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                                                {customer.type}
                                            </td>
                                            <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                                                <button 
                                                    onClick={() => submit(customer.jobId, index)}
                                                    className="block m-2 bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
                                                >
                                                    Delete
                                                </button>
                                                {/* <a href="#" className="text-indigo-600 hover:text-indigo-900">
                                                    Edit
                                                </a> */}

                                            </td>
                                        </tr>
                                    )) : null}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

        </>
    );
}
