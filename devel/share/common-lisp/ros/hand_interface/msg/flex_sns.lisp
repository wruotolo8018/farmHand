; Auto-generated. Do not edit!


(cl:in-package hand_interface-msg)


;//! \htmlinclude flex_sns.msg.html

(cl:defclass <flex_sns> (roslisp-msg-protocol:ros-message)
  ((curl1
    :reader curl1
    :initarg :curl1
    :type cl:integer
    :initform 0)
   (hype1
    :reader hype1
    :initarg :hype1
    :type cl:integer
    :initform 0)
   (curl2
    :reader curl2
    :initarg :curl2
    :type cl:integer
    :initform 0)
   (hype2
    :reader hype2
    :initarg :hype2
    :type cl:integer
    :initform 0)
   (curl3
    :reader curl3
    :initarg :curl3
    :type cl:integer
    :initform 0)
   (hype3
    :reader hype3
    :initarg :hype3
    :type cl:integer
    :initform 0)
   (curl4
    :reader curl4
    :initarg :curl4
    :type cl:integer
    :initform 0)
   (hype4
    :reader hype4
    :initarg :hype4
    :type cl:integer
    :initform 0))
)

(cl:defclass flex_sns (<flex_sns>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <flex_sns>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'flex_sns)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hand_interface-msg:<flex_sns> is deprecated: use hand_interface-msg:flex_sns instead.")))

(cl:ensure-generic-function 'curl1-val :lambda-list '(m))
(cl:defmethod curl1-val ((m <flex_sns>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hand_interface-msg:curl1-val is deprecated.  Use hand_interface-msg:curl1 instead.")
  (curl1 m))

(cl:ensure-generic-function 'hype1-val :lambda-list '(m))
(cl:defmethod hype1-val ((m <flex_sns>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hand_interface-msg:hype1-val is deprecated.  Use hand_interface-msg:hype1 instead.")
  (hype1 m))

(cl:ensure-generic-function 'curl2-val :lambda-list '(m))
(cl:defmethod curl2-val ((m <flex_sns>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hand_interface-msg:curl2-val is deprecated.  Use hand_interface-msg:curl2 instead.")
  (curl2 m))

(cl:ensure-generic-function 'hype2-val :lambda-list '(m))
(cl:defmethod hype2-val ((m <flex_sns>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hand_interface-msg:hype2-val is deprecated.  Use hand_interface-msg:hype2 instead.")
  (hype2 m))

(cl:ensure-generic-function 'curl3-val :lambda-list '(m))
(cl:defmethod curl3-val ((m <flex_sns>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hand_interface-msg:curl3-val is deprecated.  Use hand_interface-msg:curl3 instead.")
  (curl3 m))

(cl:ensure-generic-function 'hype3-val :lambda-list '(m))
(cl:defmethod hype3-val ((m <flex_sns>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hand_interface-msg:hype3-val is deprecated.  Use hand_interface-msg:hype3 instead.")
  (hype3 m))

(cl:ensure-generic-function 'curl4-val :lambda-list '(m))
(cl:defmethod curl4-val ((m <flex_sns>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hand_interface-msg:curl4-val is deprecated.  Use hand_interface-msg:curl4 instead.")
  (curl4 m))

(cl:ensure-generic-function 'hype4-val :lambda-list '(m))
(cl:defmethod hype4-val ((m <flex_sns>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hand_interface-msg:hype4-val is deprecated.  Use hand_interface-msg:hype4 instead.")
  (hype4 m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <flex_sns>) ostream)
  "Serializes a message object of type '<flex_sns>"
  (cl:let* ((signed (cl:slot-value msg 'curl1)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'hype1)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'curl2)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'hype2)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'curl3)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'hype3)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'curl4)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'hype4)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <flex_sns>) istream)
  "Deserializes a message object of type '<flex_sns>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'curl1) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'hype1) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'curl2) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'hype2) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'curl3) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'hype3) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'curl4) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'hype4) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<flex_sns>)))
  "Returns string type for a message object of type '<flex_sns>"
  "hand_interface/flex_sns")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'flex_sns)))
  "Returns string type for a message object of type 'flex_sns"
  "hand_interface/flex_sns")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<flex_sns>)))
  "Returns md5sum for a message object of type '<flex_sns>"
  "57e523c8816fb6474dc2708662828753")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'flex_sns)))
  "Returns md5sum for a message object of type 'flex_sns"
  "57e523c8816fb6474dc2708662828753")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<flex_sns>)))
  "Returns full string definition for message of type '<flex_sns>"
  (cl:format cl:nil "int32 curl1~%int32 hype1~%int32 curl2~%int32 hype2~%int32 curl3~%int32 hype3~%int32 curl4~%int32 hype4~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'flex_sns)))
  "Returns full string definition for message of type 'flex_sns"
  (cl:format cl:nil "int32 curl1~%int32 hype1~%int32 curl2~%int32 hype2~%int32 curl3~%int32 hype3~%int32 curl4~%int32 hype4~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <flex_sns>))
  (cl:+ 0
     4
     4
     4
     4
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <flex_sns>))
  "Converts a ROS message object to a list"
  (cl:list 'flex_sns
    (cl:cons ':curl1 (curl1 msg))
    (cl:cons ':hype1 (hype1 msg))
    (cl:cons ':curl2 (curl2 msg))
    (cl:cons ':hype2 (hype2 msg))
    (cl:cons ':curl3 (curl3 msg))
    (cl:cons ':hype3 (hype3 msg))
    (cl:cons ':curl4 (curl4 msg))
    (cl:cons ':hype4 (hype4 msg))
))
