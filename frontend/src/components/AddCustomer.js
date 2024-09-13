import React, { useState } from 'react';
import Modal from 'react-bootstrap/Modal';

export default function AddCustomer(props) {
    const [targetUrl, setTargetUrl] = useState('');
    const [scanType, setScanType] = useState('defaultTool');
    const [type, setType] = useState('default');
    const [show, setShow] = useState(props.show);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    function handleChange(event) {
        setType(event.target.value)
    }

    function handleToolChange(event){
        setScanType(event.target.value)
    }
    return (
        <>
            <button
                onClick={props.toggleShow}
                className="block m-2 bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
            >
                + Create a scan
            </button>

            <Modal
                show={props.show}
                onHide={handleClose}
                backdrop="static"
                keyboard={false}
            >
                <Modal.Header closeButton>
                    <Modal.Title>Create Scan</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form
                        onSubmit={(e) => {
                            e.preventDefault();
                            setTargetUrl('');
                            setScanType('defaultTool');
                            setType('default')
                            props.newScan(targetUrl, scanType, type);
                        }}
                        id="editmodal"
                        className="w-full max-w-sm"
                    >
                        <div className="md:flex md:items-center mb-6">
                            <div className="md:w-1/3">
                                <label
                                    className="block text-gray-500 font-bold md:text-right mb-1 md:mb-0 pr-4"
                                    for="targetUrl"
                                >
                                    Target URL
                                </label>
                            </div>
                            <div className="md:w-2/3">
                                <input
                                    className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                                    id="targetUrl"
                                    placeholder="https://www.google.com"
                                    type="text"
                                    value={targetUrl}
                                    onChange={(e) => {
                                        setTargetUrl(e.target.value);
                                    }}
                                />
                            </div>
                        </div>
                        <div className="md:flex md:items-center mb-6">
                            <div className="md:w-1/3">
                                <label
                                    className="block text-gray-500 font-bold md:text-right mb-1 md:mb-0 pr-4"
                                    for="scanType"
                                >
                                    Scanning Tool
                                </label>
                            </div>
                            <div className="md:w-2/3">
                            <select value={scanType} onChange={handleToolChange}>
                                    <option value="defaultTool">Please choose the scanning Tool</option>
                                    <option value="hostedscan">HostedScan</option>
                                    <option value="nessus">Nessus</option>
                                    <option value="nexpose">Nexpose</option>
                                </select>
                            
                            </div>
                        </div>
                        <div className="md:flex md:items-center mb-6">
                            <div className="md:w-1/3">
                                <label
                                    className="block text-gray-500 font-bold md:text-right mb-1 md:mb-0 pr-4"
                                    for="type"
                                >
                                    Scan Name
                                </label>
                            </div>
                            <div className="md:w-2/3">
                                <select value={type} onChange={handleChange}>
                                    <option value="default">Please choose the scan Name</option>
                                    <option value="NMAP">Network Mapping Scan</option>
                                    <option value="OWASP_ZAP_ACTIVE">Active Web Application Scan</option>
                                </select>
                            </div>
                        </div>
                    </form>
                </Modal.Body>
                <Modal.Footer>
                    <button
                        className="bg-slate-400 hover:bg-slate-500 text-white font-bold py-2 px-4 rounded"
                        onClick={props.toggleShow}
                    >
                        Close
                    </button>
                    <button
                        className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
                        form="editmodal"
                    >
                        Add
                    </button>
                </Modal.Footer>
            </Modal>
        </>
    );
}
