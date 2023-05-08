# QR-Code-based-Lock

This project aims to provide a toy-level lock for IoT learning. Its workflow is as follows:

1. Users access the Flask service on the server through their mobile phones.
2. After authentication, users will receive a time-limited UUID issued by the server.
3. The UUID will be rendered into a QR code.
4. There is a camera on the lock that can capture the QR code displayed on the mobile phone screen.
5. The camera will compare the captured QR code with the UUID stored on the server. If the comparison is successful, the lock will be opened.

## How to Use

This project includes two components: the server and the lock. Users need to deploy both components to use the lock.

### Server

The server is implemented using the Flask framework. To run the server, you need to install Python 3.x and the required Python packages using the following command:

```
pip install flask qrcode
```

Once you have installed these packages, you can run the server using the following command:

```
python server.py
```

This command will start the Flask application locally and make it accessible through http://your-ip:5000.

## Lock

To be done