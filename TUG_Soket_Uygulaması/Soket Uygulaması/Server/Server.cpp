#include <iostream>
#include <winsock2.h>

// Winsock kütüphanesini linklemek için (Visual Studio veya MinGW için)
#pragma comment(lib, "ws2_32.lib") 

int main() {
    // 1. Winsock'u Başlat
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cout << "WSAStartup basarisiz oldu!" << std::endl;
        return 1;
    }

    // 2. Soket Oluştur (IPv4, TCP)
    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == INVALID_SOCKET) {
        std::cout << "Soket olusturma hatasi!\n"; return 1;
    }

    // 3. Adres ve Port Ayarları
    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(60000);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    // 4. Soketi Porta Bağla (Bind) ve Dinlemeye Başla (Listen)
    if (bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        std::cout << "Bind hatasi! Hata Kodu: " << WSAGetLastError() << "\n";
        return 1;
    }

    if (listen(serverSocket, 1) == SOCKET_ERROR) {
        std::cout << "Listen hatasi! Hata Kodu: " << WSAGetLastError() << "\n";
        return 1;
    }

    std::cout << "Sunucu dinliyor (Port: 60000)..." << std::endl;

    // 5. İstemci Bağlantısını Kabul Et
    SOCKET clientSocket = accept(serverSocket, nullptr, nullptr);
    if (clientSocket == INVALID_SOCKET) {
        std::cout << "Accept (Baglanti kabul) hatasi! Hata Kodu: " << WSAGetLastError() << "\n";
        return 1;
    }

    // 6. Veri Alma Döngüsü
    char buffer[4096];
    int bytesReceived;
    long totalBytes = 0;

    while ((bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0)) > 0) {
        totalBytes += bytesReceived;
    }

    if (bytesReceived == SOCKET_ERROR) {
        std::cout << "Recv (Veri alma) hatasi! Hata Kodu: " << WSAGetLastError() << "\n";
    }

    std::cout << "Toplam alinan veri: " << totalBytes << " byte." << std::endl;

    // 7. Soketleri Kapat ve Temizle
    closesocket(clientSocket);
    closesocket(serverSocket);
    WSACleanup();

    return 0;
}