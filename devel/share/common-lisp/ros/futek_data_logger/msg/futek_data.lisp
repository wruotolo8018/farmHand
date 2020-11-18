; Auto-generated. Do not edit!


(cl:in-package futek_data_logger-msg)


;//! \htmlinclude futek_data.msg.html

(cl:defclass <futek_data> (roslisp-msg-protocol:ros-message)
  ((futek1
    :reader futek1
    :initarg :futek1
    :type cl:float
    :initform 0.0)
   (futek2
    :reader futek2
    :initarg :futek2
    :type cl:float
    :initform 0.0))
)

(cl:defclass futek_data (<futek_data>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <futek_data>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'futek_data)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name futek_data_logger-msg:<futek_data> is deprecated: use futek_data_logger-msg:futek_data instead.")))

(cl:ensure-generic-function 'futek1-val :lambda-list '(m))
(cl:defmethod futek1-val ((m <futek_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader futek_data_logger-msg:futek1-val is deprecated.  Use futek_data_logger-msg:futek1 instead.")
  (futek1 m))

(cl:ensure-generic-function 'futek2-val :lambda-list '(m))
(cl:defmethod futek2-val ((m <futek_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader futek_data_logger-msg:futek2-val is deprecated.  Use futek_data_logger-msg:futek2 instead.")
  (futek2 m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <futek_data>) ostream)
  "Serializes a message object of type '<futek_data>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'futek1))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'futek2))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <futek_data>) istream)
  "Deserializes a message object of type '<futek_data>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'futek1) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'futek2) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<futek_data>)))
  "Returns string type for a message object of type '<futek_data>"
  "futek_data_logger/futek_data")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'futek_data)))
  "Returns string type for a message object of type 'futek_data"
  "futek_data_logger/futek_data")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<futek_data>)))
  "Returns md5sum for a message object of type '<futek_data>"
  "0b61dc96ccfbf1e910f406986b9acb9a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'futek_data)))
  "Returns md5sum for a message object of type 'futek_data"
  "0b61dc96ccfbf1e910f406986b9acb9a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<futek_data>)))
  "Returns full string definition for message of type '<futek_data>"
  (cl:format cl:nil "float32 futek1~%float32 futek2~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'futek_data)))
  "Returns full string definition for message of type 'futek_data"
  (cl:format cl:nil "float32 futek1~%float32 futek2~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <futek_data>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <futek_data>))
  "Converts a ROS message object to a list"
  (cl:list 'futek_data
    (cl:cons ':futek1 (futek1 msg))
    (cl:cons ':futek2 (futek2 msg))
))
