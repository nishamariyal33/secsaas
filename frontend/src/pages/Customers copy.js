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
            {customers
                ? customers.map((customer,index) => {

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
                                                    Scan Type
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr class="bg-white border-b">
                                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{index}</td>
                                                <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                                                    {customer.requested_targets[0].target}
                                                </td>
                                                <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                                                    {customer.state}
                                                </td>
                                                <td class="text-sm text-gray-900 font-light px-6 py-4 whitespace-nowrap">
                                                    NMAP
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                }) : null}
        </>
    );
}
