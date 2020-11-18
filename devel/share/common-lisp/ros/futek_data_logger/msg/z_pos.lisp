; Auto-generated. Do not edit!


(cl:in-package futek_data_logger-msg)


;//! \htmlinclude z_pos.msg.html

(cl:defclass <z_pos> (roslisp-msg-protocol:ros-message)
  ((z_pos
    :reader z_pos
    :initarg :z_pos
    :type cl:float
    :initform 0.0))
)

(cl:defclass z_pos (<z_pos>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <z_pos>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'z_pos)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name futek_data_logger-msg:<z_pos> is deprecated: use futek_data_logger-msg:z_pos instead.")))

(cl:ensure-generic-function 'z_pos-val :lambda-list '(m))
(cl:defmethod z_pos-val ((m <z_pos>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader futek_data_logger-msg:z_pos-val is deprecated.  Use futek_data_logger-msg:z_pos instead.")
  (z_pos m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <z_pos>) ostream)
  "Serializes a message object of type '<z_pos>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'z_pos))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <z_pos>) istream)
  "Deserializes a message object of type '<z_pos>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'z_pos) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<z_pos>)))
  "Returns string type for a message object of type '<z_pos>"
  "futek_data_logger/z_pos")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'z_pos)))
  "Returns string type for a message object of type 'z_pos"
  "futek_data_logger/z_pos")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<z_pos>)))
  "Returns md5sum for a message object of type '<z_pos>"
  "2b07eb162418378344d3a01a88af5f3c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'z_pos)))
  "Returns md5sum for a message object of type 'z_pos"
  "2b07eb162418378344d3a01a88af5f3c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<z_pos>)))
  "Returns full string definition for message of type '<z_pos>"
  (cl:format cl:nil "float32 z_pos~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'z_pos)))
  "Returns full string definition for message of type 'z_pos"
  (cl:format cl:nil "float32 z_pos~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <z_pos>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <z_pos>))
  "Converts a ROS message object to a list"
  (cl:list 'z_pos
    (cl:cons ':z_pos (z_pos msg))
))
