git clone https://github.com/FujishigeTemma/LabRotations.git
mv LabRotations/NCBC/* ./
rm -rf LabRotations

sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
curl -sSf https://rye-up.com/get | bash
echo '. "$HOME/.rye/env"' >>~/.bashrc
. ~/.bashrc

rm /usr/local/lib/libtbbbind.so.3
ln -s /usr/local/lib/libtbbbind.so.3.10 /usr/local/lib/libtbbbind.so.3

rm /usr/local/lib/libtbb.so.12
ln -s /usr/local/lib/libtbb.so.12.10 /usr/local/lib/libtbb.so.12

rm /usr/local/lib/libtbbbind_2_0.so.3
ln -s /usr/local/lib/libtbbbind_2_0.so.3.10 /usr/local/lib/libtbbbind_2_0.so.3

rm /usr/local/lib/libtbbbind_2_5.so.3
ln -s /usr/local/lib/libtbbbind_2_5.so.3.10 /usr/local/lib/libtbbbind_2_5.so.3

rm /usr/local/lib/libtbbmalloc.so.2
ln -s /usr/local/lib/libtbbmalloc.so.2.10 /usr/local/lib/libtbbmalloc.so.2

rm /usr/local/lib/libtbbmalloc_proxy.so.2
ln /usr/local/lib/libtbbmalloc_proxy.so.2.10 /usr/local/lib/libtbbmalloc_proxy.so.2

curl https://developer.download.nvidia.com/hpc-sdk/ubuntu/DEB-GPG-KEY-NVIDIA-HPC-SDK | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-hpcsdk-archive-keyring.gpg
echo 'deb [signed-by=/usr/share/keyrings/nvidia-hpcsdk-archive-keyring.gpg] https://developer.download.nvidia.com/hpc-sdk/ubuntu/amd64 /' | sudo tee /etc/apt/sources.list.d/nvhpc.list
apt-get update -y && apt-get install -y nvhpc-22-1

rye remove neuron && rye add neuron-gpu
rye sync
