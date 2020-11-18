;; Auto-generated. Do not edit!


(when (boundp 'futek_data_logger::z_pos)
  (if (not (find-package "FUTEK_DATA_LOGGER"))
    (make-package "FUTEK_DATA_LOGGER"))
  (shadow 'z_pos (find-package "FUTEK_DATA_LOGGER")))
(unless (find-package "FUTEK_DATA_LOGGER::Z_POS")
  (make-package "FUTEK_DATA_LOGGER::Z_POS"))

(in-package "ROS")
;;//! \htmlinclude z_pos.msg.html


(defclass futek_data_logger::z_pos
  :super ros::object
  :slots (_z_pos ))

(defmethod futek_data_logger::z_pos
  (:init
   (&key
    ((:z_pos __z_pos) 0.0)
    )
   (send-super :init)
   (setq _z_pos (float __z_pos))
   self)
  (:z_pos
   (&optional __z_pos)
   (if __z_pos (setq _z_pos __z_pos)) _z_pos)
  (:serialization-length
   ()
   (+
    ;; float32 _z_pos
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _z_pos
       (sys::poke _z_pos (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _z_pos
     (setq _z_pos (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get futek_data_logger::z_pos :md5sum-) "2b07eb162418378344d3a01a88af5f3c")
(setf (get futek_data_logger::z_pos :datatype-) "futek_data_logger/z_pos")
(setf (get futek_data_logger::z_pos :definition-)
      "float32 z_pos

")



(provide :futek_data_logger/z_pos "2b07eb162418378344d3a01a88af5f3c")


