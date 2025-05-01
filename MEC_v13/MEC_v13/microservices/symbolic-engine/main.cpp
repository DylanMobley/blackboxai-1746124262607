#include <opencog/atoms/AtomSpace.h>
#include <opencog/atomese/CodeLoader.h>
#include <iostream>
#include <csignal>
#include "zmq_router.h"

using namespace opencog;

// Global pointer for shutdown
AtomSpace* atomspace = nullptr;
bool running = true;

// Handle Ctrl+C clean shutdown
void signalHandler(int signum) {
    std::cout << "\n[Shutdown] Signal (" << signum << ") received. Cleaning up..." << std::endl;
    running = false;
}

int main() {
    std::cout << "[MEC_v13+] Starting Symbolic Engine..." << std::endl;

    // 1. Initialize AtomSpace
    atomspace = new AtomSpace();

    // 2. Load startup rules
    CodeLoader loader(atomspace);
    try {
        loader.loadAtomeseFile("startup_rules.scm");
        std::cout << "[✓] RulePack loaded from startup_rules.scm" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "[✗] Failed to load RulePacks: " << e.what() << std::endl;
        return 1;
    }

    // 3. Register shutdown handler
    signal(SIGINT, signalHandler);

    // 4. Launch ZMQ server (defined in zmq_router.cpp)
    std::cout << "[ZMQ] Listening for symbolic payloads..." << std::endl;
    while (running) {
        try {
            pollZMQ(atomspace);  // ⬅️ Blocking router handler
        } catch (const std::exception& ex) {
            std::cerr << "[Error] ZMQ Router Error: " << ex.what() << std::endl;
        }
    }

    std::cout << "[✓] Symbolic Engine shut down gracefully." << std::endl;
    delete atomspace;
    return 0;
}
