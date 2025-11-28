

const URL = "http://localhost:8000"

export async function list_s3_objects() {
    try {
        const response = await fetch(`${URL}/api/v1/list`)
        if (!response.ok) {
            throw new Error(`Error: ${response.status}`)
        }
        const data = await response.json();
        return data
    } catch (error) {
        console.error("error:", error);
        throw error;
    }
}

export function convert_bytes(size) {
    if (size < 1024 * 1024) {
        return `${Math.floor(size / 1024)} KB`
    }
    else if (size < 1024 * 1024 * 1024) {
        return `${Math.floor(size / (1024 * 1024))} MB`
    }
    else {
        return `${(size / (1024 * 1024 * 1024)).toFixed(2)} GB`
    }
}

export async function upload_file(file_data) {

    const formData = new FormData();
    formData.append('file', file_data);

    try {
        const response = await fetch(`${URL}/api/v1/upload`, {
            method: "POST",
            body: formData
        }
        )
        if (!response.ok) {
            throw new Error(`Reponse status: ${response.status}`)
        }
    } catch (error) {
        console.error(`error: ${error}`)
        throw error
    }
}