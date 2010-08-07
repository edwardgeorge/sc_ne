from stdlib cimport *
from python cimport *

cdef extern from "CoreFoundation/CFBase.h":
    ctypedef unsigned char Boolean
    ctypedef unsigned int Byte
    ctypedef unsigned short UInt16
    ctypedef unsigned int UInt32
    ctypedef unsigned long UInt64
    ctypedef unsigned int OSStatus
    ctypedef void* CFTypeRef
    ctypedef CFTypeRef CFStringRef

cdef extern from "CoreFoundation/CFString.h":
    ctypedef UInt32 CFStringEncoding

    CFStringRef CFStringCreateWithCString(
        void* alloc,
        char* cStr,
        CFStringEncoding encoding)

    Boolean CFStringGetCString(
        CFStringRef theString,
        char *buffer,
        int bufferSize,
        CFStringEncoding encoding)

    void CFRelease(CFTypeRef cf)

cdef extern from "CoreMIDI/MIDIServices.h":
    ctypedef void* MIDIObjectRef
    ctypedef MIDIObjectRef MIDINotification
    ctypedef MIDIObjectRef MIDIClientRef
    ctypedef MIDIObjectRef MIDIDeviceRef
    ctypedef MIDIObjectRef MIDIEndpointRef
    ctypedef MIDIObjectRef MIDIPortRef

    ctypedef UInt64 MIDITimeStamp

    ctypedef struct MIDIPacket:
        MIDITimeStamp timeStamp
        UInt16 length
        Byte data[256]

    ctypedef struct MIDIPacketList:
        UInt32       numPackets
        MIDIPacket*   packet

    ctypedef void (*MIDINotifyProc)(MIDINotification *message, void *refCon)
    ctypedef void (*MIDIReadProc)(MIDIPacketList *pktlist, void *readProcRefCon,
        void *srcConnRefCon)

    OSStatus MIDIClientCreate(
        CFStringRef name,
        MIDINotifyProc notifyProc,
        void* notifyRefCon,
        MIDIClientRef* outClient) 

    OSStatus MIDISourceCreate(
        MIDIClientRef client,
        CFStringRef name,
        MIDIEndpointRef* outsrc)

    OSStatus MIDIInputPortCreate(
        MIDIClientRef client,
        CFStringRef portName,
        MIDIReadProc readProc,
        void* refCon,
        MIDIPortRef* outPort)

    OSStatus MIDIOutputPortCreate(
        MIDIClientRef client,
        CFStringRef portName,
        MIDIPortRef* outPort)

    OSStatus MIDIPortConnectSource(
        MIDIPortRef port,
        MIDIEndpointRef source,
        void* connRefCon)

    OSStatus MIDIObjectGetStringProperty(
        MIDIObjectRef obj,
        CFStringRef propertyID,
        CFStringRef* str)

    MIDIPacket* MIDIPacketNext(MIDIPacket *pkt)

    int MIDIGetNumberOfDevices()
    int MIDIGetNumberOfSources()
    int MIDIGetNumberOfDestinations()

    MIDIDeviceRef MIDIGetDevice(
        int deviceIndex0)

    MIDIEndpointRef MIDIGetSource(
        int sourceIndex0)

    MIDIEndpointRef MIDIGetDestination(
        int destIndex0)

    CFStringRef kMIDIPropertyName
    CFStringRef kMIDIPropertyDisplayName
    CFStringRef kMIDIPropertyManufacturer
    CFStringRef kMIDIPropertyModel

cdef extern from "Python.h":
    void PyEval_InitThreads()
    ctypedef int PyGILState_STATE
    PyGILState_STATE PyGILState_Ensure()
    void PyGILState_Release(PyGILState_STATE gstate)

cdef CFStringRef cfstr(char* cstr):
    return CFStringCreateWithCString(NULL, cstr, 0)

cdef struct programdata:
    void* callback
    void* data

def getnumsources():
    return MIDIGetNumberOfSources()

def getnumdestinations():
    return MIDIGetNumberOfDestinations()

def getnumdevices():
    return MIDIGetNumberOfDevices()

cdef char* getproperty(MIDIObjectRef obj, CFStringRef prop):
    cdef CFStringRef pval
    cdef char val[64]
    MIDIObjectGetStringProperty(obj, prop, &pval)
    CFStringGetCString(pval, val, sizeof(val), 0)
    CFRelease(pval)
    return val

def getdeviceinfo(int devid):
    cdef MIDIDeviceRef dev = MIDIGetDevice(devid)
    cdef CFStringRef *props = [kMIDIPropertyName, kMIDIPropertyManufacturer, kMIDIPropertyModel]

    ret = []
    for i in range(3):
        ret.append(getproperty(dev, props[i]))
    return ret

def getsourceinfo(int sourceid):
    cdef MIDIEndpointRef src
    src = MIDIGetSource(sourceid)
    cdef CFStringRef *props = [kMIDIPropertyDisplayName, kMIDIPropertyManufacturer, kMIDIPropertyModel]

    ret = []
    for i in range(3):
        ret.append(getproperty(src, props[i]))
    return ret

cdef void callback(MIDIPacketList *pktlist, void *refCon, void *connRefCon):
    cdef programdata *td = <programdata*>refCon
    cdef MIDIPacket *packet = <MIDIPacket *>pktlist.packet
    cdef int i

    cdef PyGILState_STATE gil
    for i in range(pktlist.numPackets):
        gil = PyGILState_Ensure()
        print 'unknown:', hex(packet.data[0])
        PyGILState_Release(gil)

        packet = MIDIPacketNext(packet)

cdef void callbacktopython(void* callback, unsigned long clockpos, float bpm) with gil:
    (<object>callback)(clockpos, bpm)

def go(object callbackfunc, object data):
    PyEval_InitThreads()

    cdef programdata *td = <programdata*>malloc(sizeof(programdata))
    cdef int i
    cdef MIDIClientRef client
    cdef MIDIPortRef inport

    td.callback = <void*>callbackfunc
    td.data = <void*>data

    MIDIClientCreate(cfstr("test"), NULL, NULL, &client)
    MIDIInputPortCreate(client, cfstr("input"), callback, <void*>td, &inport)

    cdef int numsources = MIDIGetNumberOfSources()
    cdef MIDIEndpointRef src
    for i in range(numsources):
        src = MIDIGetSource(i)
        print getproperty(src, kMIDIPropertyName)
        MIDIPortConnectSource(inport, src, NULL)

