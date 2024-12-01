# Install the Google Cloud CLI

Link :https://cloud.google.com/sdk/docs/install-sdk#linux


1. To download the Linux archive file, run the following command:
ใช้สำหรับดาวน์โหลดไฟล์ติดตั้ง Google Cloud CLI สำหรับระบบปฏิบัติการ Linux แบบ 64-bit

```
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz

```

2.To extract the contents of the file to your file system (preferably to your home directory), run the following command:

```
tar -xf google-cloud-cli-linux-x86_64.tar.gz
```
4.Add the gcloud CLI to your path. Run the installation script from the root of the folder you extracted to using the following command:

```
./google-cloud-sdk/install.sh
```

5. Add gcloud command 
```
echo 'export PATH=$PATH:./google-cloud-sdk/bin' >> ~/.bashrc
source ~/.bashrc
```