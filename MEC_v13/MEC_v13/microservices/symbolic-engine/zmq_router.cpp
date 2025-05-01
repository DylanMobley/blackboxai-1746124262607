#include <zmq.h>
#include <zmq.hpp>
#include <iostream>
#include <string>
#include <opencog/atoms/AtomSpace.h>
#include <opencog/atomese/CodeEvaluator.h>
#include <opencog/util/StringTokenizer.h>

using namespace opencog;

void pollZMQ(AtomSpace* atomspace) {
    zmq::context_t context(1);
    zmq::socket_t socket(context, ZMQ_REP);
    socket.bind("tcp://*:5555");

    std::cout << "[ZMQ] Listening on tcp://*:5555 for symbolic payloads..." << std::endl;

    while (true) {
        zmq::message_t request;

        // 1. Wait for message
        socket.recv(&request);
        std::string scheme_input(static_cast<char*>(request.data()), request.size());

        std::cout << "[ZMQ] Received payload:\n" << scheme_input << "\n";

        try {
            // 2. Parse and execute Scheme string in AtomSpace
            CodeEvaluator evaluator(atomspace);
            evaluator.eval(scheme_input);

            // 3. Respond to client
            std::string response = "[✓] Symbolic payload processed.";
            zmq::message_t reply(response.size());
            memcpy(reply.data(), response.c_str(), response.size());
            socket.send(reply);
        } catch (const std::exception& ex) {
            std::cerr << "[Error] Symbolic execution failed: " << ex.what() << std::endl;
            std::string response = std::string("[✗] Error: ") + ex.what();
            zmq::message_t reply(response.size());
            memcpy(reply.data(), response.c_str(), response.size());
            socket.send(reply);
        }
    }
}
