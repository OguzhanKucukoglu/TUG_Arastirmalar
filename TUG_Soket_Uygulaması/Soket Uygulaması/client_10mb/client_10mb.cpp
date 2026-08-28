#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include <iostream>
#include <vector>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")


int main() {
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cout << "WSAStartup basarisiz oldu!" << std::endl;
        return 1;
    }

    SOCKET clientSocket = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(60000);
    inet_pton(AF_INET, "127.0.0.1", &serverAddr.sin_addr);

    connect(clientSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr));

    // 10 MB'lık sahte veri oluştur
    int size = 10 * 1024 * 1024;
    std::vector<char> data(size, 'A');

    int totalSent = 0;
    int bytesLeft = size;
    int chunkSize = 4096; // 4 KB'lık paketler halinde gönder

    std::cout << "10 MB veri gonderimi basliyor..." << std::endl;

    // Veri bitene kadar döngü ile gönder
    while (bytesLeft > 0) {
        int toSend = (bytesLeft < chunkSize) ? bytesLeft : chunkSize;
        int sent = send(clientSocket, data.data() + totalSent, toSend, 0);

        if (sent == SOCKET_ERROR) {
            std::cout << "Gonderim hatasi!" << std::endl;
            break;
        }
        totalSent += sent;
        bytesLeft -= sent;
    }

    std::cout << "Toplam gonderilen veri: " << totalSent << " byte." << std::endl;

    closesocket(clientSocket);
    WSACleanup();
    return 0;
}