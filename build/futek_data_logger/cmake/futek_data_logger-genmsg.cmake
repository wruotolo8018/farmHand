# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "futek_data_logger: 1 messages, 0 services")

set(MSG_I_FLAGS "-Ifutek_data_logger:/home/bdml/farmHand/src/futek_data_logger/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(futek_data_logger_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/bdml/farmHand/src/futek_data_logger/msg/futek_data.msg" NAME_WE)
add_custom_target(_futek_data_logger_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "futek_data_logger" "/home/bdml/farmHand/src/futek_data_logger/msg/futek_data.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(futek_data_logger
  "/home/bdml/farmHand/src/futek_data_logger/msg/futek_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/futek_data_logger
)

### Generating Services

### Generating Module File
_generate_module_cpp(futek_data_logger
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/futek_data_logger
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(futek_data_logger_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(futek_data_logger_generate_messages futek_data_logger_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/bdml/farmHand/src/futek_data_logger/msg/futek_data.msg" NAME_WE)
add_dependencies(futek_data_logger_generate_messages_cpp _futek_data_logger_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(futek_data_logger_gencpp)
add_dependencies(futek_data_logger_gencpp futek_data_logger_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS futek_data_logger_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(futek_data_logger
  "/home/bdml/farmHand/src/futek_data_logger/msg/futek_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/futek_data_logger
)

### Generating Services

### Generating Module File
_generate_module_eus(futek_data_logger
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/futek_data_logger
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(futek_data_logger_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(futek_data_logger_generate_messages futek_data_logger_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/bdml/farmHand/src/futek_data_logger/msg/futek_data.msg" NAME_WE)
add_dependencies(futek_data_logger_generate_messages_eus _futek_data_logger_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(futek_data_logger_geneus)
add_dependencies(futek_data_logger_geneus futek_data_logger_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS futek_data_logger_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(futek_data_logger
  "/home/bdml/farmHand/src/futek_data_logger/msg/futek_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/futek_data_logger
)

### Generating Services

### Generating Module File
_generate_module_lisp(futek_data_logger
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/futek_data_logger
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(futek_data_logger_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(futek_data_logger_generate_messages futek_data_logger_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/bdml/farmHand/src/futek_data_logger/msg/futek_data.msg" NAME_WE)
add_dependencies(futek_data_logger_generate_messages_lisp _futek_data_logger_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(futek_data_logger_genlisp)
add_dependencies(futek_data_logger_genlisp futek_data_logger_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS futek_data_logger_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(futek_data_logger
  "/home/bdml/farmHand/src/futek_data_logger/msg/futek_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/futek_data_logger
)

### Generating Services

### Generating Module File
_generate_module_nodejs(futek_data_logger
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/futek_data_logger
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(futek_data_logger_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(futek_data_logger_generate_messages futek_data_logger_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/bdml/farmHand/src/futek_data_logger/msg/futek_data.msg" NAME_WE)
add_dependencies(futek_data_logger_generate_messages_nodejs _futek_data_logger_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(futek_data_logger_gennodejs)
add_dependencies(futek_data_logger_gennodejs futek_data_logger_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS futek_data_logger_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(futek_data_logger
  "/home/bdml/farmHand/src/futek_data_logger/msg/futek_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/futek_data_logger
)

### Generating Services

### Generating Module File
_generate_module_py(futek_data_logger
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/futek_data_logger
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(futek_data_logger_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(futek_data_logger_generate_messages futek_data_logger_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/bdml/farmHand/src/futek_data_logger/msg/futek_data.msg" NAME_WE)
add_dependencies(futek_data_logger_generate_messages_py _futek_data_logger_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(futek_data_logger_genpy)
add_dependencies(futek_data_logger_genpy futek_data_logger_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS futek_data_logger_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/futek_data_logger)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/futek_data_logger
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(futek_data_logger_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/futek_data_logger)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/futek_data_logger
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(futek_data_logger_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/futek_data_logger)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/futek_data_logger
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(futek_data_logger_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/futek_data_logger)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/futek_data_logger
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(futek_data_logger_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/futek_data_logger)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/futek_data_logger\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/futek_data_logger
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(futek_data_logger_generate_messages_py std_msgs_generate_messages_py)
endif()
