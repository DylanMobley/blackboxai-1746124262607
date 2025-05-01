cmake_minimum_required(VERSION 3.10)
project(MEC_SymbolicEngine)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCog REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(ZMQ REQUIRED libzmq)

include_directories(${ZMQ_INCLUDE_DIRS})
link_directories(${ZMQ_LIBRARY_DIRS})

add_executable(symbolic_engine main.cpp zmq_router.cpp)

target_link_libraries(symbolic_engine
    ${ZMQ_LIBRARIES}
    opencog
)
