import { useEffect, useState, useContext } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import AddCustomer from '../components/AddCustomer';
import { baseUrl } from '../shared';
import { LoginContext } from '../App';
import useFetch from '../hooks/UseFetch';

export default function Customers() {
    const [loggedIn, setLoggedIn] = useContext(LoginContext);
    // const [customers, setCustomers] = useState();
    const [show, setShow] = useState(false);

    function toggleShow() {
        setShow(!show);
    }

    const location = useLocation();
    const navigate = useNavigate();

    const url = baseUrl + 'api/customers/';
    const {
        request,
        appendData,
        data: { customers } = {},
        errorStatus,
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

    function newScan(targetUrl, scanType) {
        appendData({ targetUrl: targetUrl, scanType: scanType });

        if (!errorStatus) {
            toggleShow();
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
            <div className="flex flex-col">
                <div className="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                    <div className="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
                        <div className="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th
                                            scope="col"
                                            className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                        >
                                            #
                                        </th>
                                        <th
                                            scope="col"
                                            className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                        >
                                            Target
                                        </th>
                                        <th
                                            scope="col"
                                            className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                        >
                                            Status
                                        </th>
                                        <th
                                            scope="col"
                                            className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                        >
                                            Scan Type
                                        </th>
                                        <th scope="col" className="relative px-6 py-3">
                                            <span className="sr-only">Edit</span>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {customers?customers.map((customer,index) => (
                                        <tr>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className="flex items-center">
                                                    <div className="ml-4">
                                                        <div className="text-sm font-medium text-gray-900">{index+1}</div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className="text-sm text-gray-900">{customer.requested_targets[0].target}</div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <span
                                                    className="px-2 inline-flex text-xs leading-5
                      font-semibold rounded-full bg-green-100 text-green-800"
                                                >
                                                     {customer.state}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                               NMAP
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                                <a href="#" className="text-indigo-600 hover:text-indigo-900">
                                                    Edit
                                                </a>
                                            </td>
                                        </tr>
                                    )):null}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
