
(cl:in-package :asdf)

(defsystem "hand_interface-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "flex_sns" :depends-on ("_package_flex_sns"))
    (:file "_package_flex_sns" :depends-on ("_package"))
  ))