import { list_s3_objects, convert_bytes, upload_file } from "./functions"
import { useState, useEffect } from "react"
import styles from "./Scanner.module.css"
import Button from "react-bootstrap/Button"
import Card from 'react-bootstrap/Card';
import Alert from 'react-bootstrap/Alert';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css';

function Scanner() {
    const [objectList, setObjectList] = useState([]);
    const [fileUploadFormData, setFileUploadFormData] = useState(null);
    const [alert, setAlert] = useState(null)

    const fetch_list = async () => {
        try {
            const result = await list_s3_objects();
            setObjectList(result);
        } catch (error) {
            console.log(`error: ${error}`)
            throw error
        }
    }

    const upload_file_handler = async () => {

        try {
            await upload_file(fileUploadFormData);
            setAlert({ type: "success", message: "File Upload Successful!" })
        } catch (error) {
            setAlert({ type: "danger", message: "File Upload Unsuccessful" })
            console.error("error: ", error)
            throw error;
        }
    }

    const file_form_handler = (data) => {
        setFileUploadFormData(data)
    }

    useEffect(() => {
        fetch_list();
    }, [])

    return (
        <>
            <>
                <Card>
                    <Card.Header as="h5" variant="dark">File Scanner</Card.Header>
                    <InputGroup className="mb-3">
                        <Form.Control
                            type="file"
                            aria-label="Default"
                            aria-describedby="inputGroup-sizing-default"
                            onChange={(e) => file_form_handler(e.target.files[0])}
                        />
                    </InputGroup>
                    {alert && (
                        <Alert
                            variant={alert.type}
                            onClose={() => setAlert(null)}
                            dismissible
                            className="mb-3"
                        >
                            {alert.message}
                        </Alert>
                    )}
                    <Button variant="primary" onClick={upload_file_handler}>Upload</Button>
                    <Card.Body>
                        <Card.Title>{objectList.length} =  Clean Files</Card.Title>
                        <table className={styles.objectTable}>
                            <thead>
                                <tr>
                                    <th className={styles.objectTableHeader}>File</th>
                                    <th>Size</th>
                                </tr>
                            </thead>
                            <tbody>
                                {objectList.map((file, index) =>
                                    <tr key={index}>
                                        <td>
                                            {file.Key}
                                        </td>
                                        <td>{convert_bytes(file.Size)}</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </Card.Body>
                </Card>
            </>
        </>
    )
}

export default Scanner