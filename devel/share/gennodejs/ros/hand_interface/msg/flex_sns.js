// Auto-generated. Do not edit!

// (in-package hand_interface.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class flex_sns {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.curl1 = null;
      this.hype1 = null;
      this.curl2 = null;
      this.hype2 = null;
      this.curl3 = null;
      this.hype3 = null;
      this.curl4 = null;
      this.hype4 = null;
    }
    else {
      if (initObj.hasOwnProperty('curl1')) {
        this.curl1 = initObj.curl1
      }
      else {
        this.curl1 = 0;
      }
      if (initObj.hasOwnProperty('hype1')) {
        this.hype1 = initObj.hype1
      }
      else {
        this.hype1 = 0;
      }
      if (initObj.hasOwnProperty('curl2')) {
        this.curl2 = initObj.curl2
      }
      else {
        this.curl2 = 0;
      }
      if (initObj.hasOwnProperty('hype2')) {
        this.hype2 = initObj.hype2
      }
      else {
        this.hype2 = 0;
      }
      if (initObj.hasOwnProperty('curl3')) {
        this.curl3 = initObj.curl3
      }
      else {
        this.curl3 = 0;
      }
      if (initObj.hasOwnProperty('hype3')) {
        this.hype3 = initObj.hype3
      }
      else {
        this.hype3 = 0;
      }
      if (initObj.hasOwnProperty('curl4')) {
        this.curl4 = initObj.curl4
      }
      else {
        this.curl4 = 0;
      }
      if (initObj.hasOwnProperty('hype4')) {
        this.hype4 = initObj.hype4
      }
      else {
        this.hype4 = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type flex_sns
    // Serialize message field [curl1]
    bufferOffset = _serializer.int32(obj.curl1, buffer, bufferOffset);
    // Serialize message field [hype1]
    bufferOffset = _serializer.int32(obj.hype1, buffer, bufferOffset);
    // Serialize message field [curl2]
    bufferOffset = _serializer.int32(obj.curl2, buffer, bufferOffset);
    // Serialize message field [hype2]
    bufferOffset = _serializer.int32(obj.hype2, buffer, bufferOffset);
    // Serialize message field [curl3]
    bufferOffset = _serializer.int32(obj.curl3, buffer, bufferOffset);
    // Serialize message field [hype3]
    bufferOffset = _serializer.int32(obj.hype3, buffer, bufferOffset);
    // Serialize message field [curl4]
    bufferOffset = _serializer.int32(obj.curl4, buffer, bufferOffset);
    // Serialize message field [hype4]
    bufferOffset = _serializer.int32(obj.hype4, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type flex_sns
    let len;
    let data = new flex_sns(null);
    // Deserialize message field [curl1]
    data.curl1 = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [hype1]
    data.hype1 = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [curl2]
    data.curl2 = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [hype2]
    data.hype2 = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [curl3]
    data.curl3 = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [hype3]
    data.hype3 = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [curl4]
    data.curl4 = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [hype4]
    data.hype4 = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 32;
  }

  static datatype() {
    // Returns string type for a message object
    return 'hand_interface/flex_sns';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '57e523c8816fb6474dc2708662828753';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 curl1
    int32 hype1
    int32 curl2
    int32 hype2
    int32 curl3
    int32 hype3
    int32 curl4
    int32 hype4
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new flex_sns(null);
    if (msg.curl1 !== undefined) {
      resolved.curl1 = msg.curl1;
    }
    else {
      resolved.curl1 = 0
    }

    if (msg.hype1 !== undefined) {
      resolved.hype1 = msg.hype1;
    }
    else {
      resolved.hype1 = 0
    }

    if (msg.curl2 !== undefined) {
      resolved.curl2 = msg.curl2;
    }
    else {
      resolved.curl2 = 0
    }

    if (msg.hype2 !== undefined) {
      resolved.hype2 = msg.hype2;
    }
    else {
      resolved.hype2 = 0
    }

    if (msg.curl3 !== undefined) {
      resolved.curl3 = msg.curl3;
    }
    else {
      resolved.curl3 = 0
    }

    if (msg.hype3 !== undefined) {
      resolved.hype3 = msg.hype3;
    }
    else {
      resolved.hype3 = 0
    }

    if (msg.curl4 !== undefined) {
      resolved.curl4 = msg.curl4;
    }
    else {
      resolved.curl4 = 0
    }

    if (msg.hype4 !== undefined) {
      resolved.hype4 = msg.hype4;
    }
    else {
      resolved.hype4 = 0
    }

    return resolved;
    }
};

module.exports = flex_sns;
