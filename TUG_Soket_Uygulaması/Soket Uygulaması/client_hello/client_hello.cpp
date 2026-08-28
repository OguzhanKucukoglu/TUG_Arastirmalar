#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include <iostream>
#include <string>
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
    inet_pton(AF_INET, "127.0.0.1", &serverAddr.sin_addr); // Localhost'a bağlan

    // Sunucuya bağlan (3-way handshake burada gerçekleşir)
    if (connect(clientSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cout << "Sunucuya baglanilamadi! Hata Kodu: " << WSAGetLastError() << "\n";
        closesocket(clientSocket);
        WSACleanup();
        return 1;
    }

    // Veriyi gönder
    std::string message = "Hello World";
    send(clientSocket, message.c_str(), static_cast<int>(message.length()), 0);
    std::cout << "Mesaj gonderildi: " << message << std::endl;

    // Bağlantıyı kapat (FIN paketi gönderilir)
    closesocket(clientSocket);
    WSACleanup();
    return 0;
}