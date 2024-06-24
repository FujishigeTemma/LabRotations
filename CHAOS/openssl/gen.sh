openssl genrsa -out localhost.key
openssl req -new -key localhost.key -out localhost.csr -subj "/CN=localhost"
openssl x509 -req -days 365 -in localhost.csr -signkey localhost.key -out localhost.crt -extfile san.txt
