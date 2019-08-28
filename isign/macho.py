#
# Constructs to represent various structures
# in a Mach-O binary.
#
# As with all Constructs, can be used for both
# parsing or emitting (aka building)
#


from construct import *
from macho_cs import Blob

UInt32 = ULInt32
UInt64 = ULInt64

CodeSigRef = Struct("codesig",
                    UInt32('dataoff'),
                    UInt32('datasize'),
                    )

Segment = Struct('segment',
                                                       PaddedStringAdapter(Bytes('segname', 16)),
                                                       UInt32('vmaddr'),
                                                       UInt32('vmsize'),
                                                       UInt32('fileoff'),
                                                       UInt32('filesize'),
                                                       UInt32('maxprot'),
                                                       UInt32('initprot'),
                                                       UInt32('nsects'),
                                                       UInt32('flags'),
                                                       Rename("sections",
                                                              Array(lambda ctx: ctx['nsects'],
                                                                    Struct('Section',
                                                                           PaddedStringAdapter(Bytes('sectname', 16)),
                                                                           PaddedStringAdapter(Bytes('segname', 16)),
                                                                           UInt64('addr'),
                                                                           UInt64('size'),
                                                                           UInt32('offset'),
                                                                           UInt32('align'),
                                                                           UInt32('reloff'),
                                                                           UInt32('nreloc'),
                                                                           UInt32('flags'),
                                                                           UInt32('reserved1'),
                                                                           UInt32('reserved2'),
                                                                           UInt32('reserved3'),
                                                                           ))),
                                                       )

Segment64 = Struct('segment',
                                                       PaddedStringAdapter(Bytes('segname', 16)),
                                                       UInt64('vmaddr'),
                                                       UInt64('vmsize'),
                                                       UInt64('fileoff'),
                                                       UInt64('filesize'),
                                                       UInt32('maxprot'),
                                                       UInt32('initprot'),
                                                       UInt32('nsects'),
                                                       UInt32('flags'),
                                                       Rename("sections",
                                                              Array(lambda ctx: ctx['nsects'],
                                                                    Struct('Section',
                                                                           PaddedStringAdapter(Bytes('sectname', 16)),
                                                                           PaddedStringAdapter(Bytes('segname', 16)),
                                                                           UInt64('addr'),
                                                                           UInt64('size'),
                                                                           UInt32('offset'),
                                                                           UInt32('align'),
                                                                           UInt32('reloff'),
                                                                           UInt32('nreloc'),
                                                                           UInt32('flags'),
                                                                           UInt32('reserved1'),
                                                                           UInt32('reserved2'),
                                                                           UInt32('reserved3'),
                                                                           ))),
                                                       )

LoadCommand = Struct("LoadCommand",
                     Enum(UInt32("cmd"),
                          LC_SEGMENT=0x1,
                          LC_SYMTAB=0x2,
                          LC_SYMSEG=0x3,
                          LC_THREAD=0x4,
                          LC_UNIXTHREAD=0x5,
                          LC_LOADFVMLIB=0x6,
                          LC_IDFVMLIB=0x7,
                          LC_IDENT=0x8,
                          LC_FVMFILE=0x9,
                          LC_PREPAGE=0xa,
                          LC_DYSYMTAB=0xb,
                          LC_LOAD_DYLIB=0xc,
                          LC_ID_DYLIB=0xd,
                          LC_LOAD_DYLINKER=0xe,
                          LC_ID_DYLINKER=0xf,
                          LC_PREBOUND_DYLIB=0x10,
                          LC_ROUTINES=0x11,
                          LC_SUB_FRAMEWORK=0x12,
                          LC_SUB_UMBRELLA=0x13,
                          LC_SUB_CLIENT=0x14,
                          LC_SUB_LIBRARY=0x15,
                          LC_TWOLEVEL_HINTS=0x16,
                          LC_PREBIND_CKSUM=0x17,
                          LC_LOAD_WEAK_DYLIB=0x80000018,
                          LC_SEGMENT_64=0x19,
                          LC_ROUTINES_64=0x1a,
                          LC_UUID=0x1b,
                          LC_RPATH=0x8000001c,
                          LC_CODE_SIGNATURE=0x1d,
                          LC_SEGMENT_SPLIT_INFO=0x1e,
                          LC_REEXPORT_DYLIB=0x8000001f,
                          LC_LAZY_LOAD_DYLIB=0x20,
                          LC_ENCRYPTION_INFO=0x21,
                          LC_DYLD_INFO=0x22,
                          LC_DYLD_INFO_ONLY=0x80000022,
                          LC_LOAD_UPWARD_DYLIB=0x80000023,
                          LC_VERSION_MIN_MACOSX=0x24,
                          LC_VERSION_MIN_IPHONEOS=0x25,
                          LC_FUNCTION_STARTS=0x26,
                          LC_DYLD_ENVIRONMENT=0x27,
                          LC_MAIN=0x80000028,
                          LC_DATA_IN_CODE=0x29,
                          LC_SOURCE_VERSION=0x2a,
                          LC_DYLIB_CODE_SIGN_DRS=0x2b,
                          LC_ENCRYPTION_INFO_64=0x2c,
                          LC_LINKER_OPTION=0x2d,
                          LC_LINKER_OPTIMIZATION_HINT=0x2e,
                          LC_VERSION_MIN_TVOS=0x2f,
                          LC_VERSION_MIN_WATCHOS=0x30,
                          LC_NOTE=0x31,
                          LC_BUILD_VERSION=0x32,
                          ),

                     UInt32("cmdsize"),
                     Peek(Switch("data", lambda ctx: ctx['cmd'],
                                 {'LC_SEGMENT': Struct('segment',
                                                       PaddedStringAdapter(Bytes('segname', 16)),
                                                       UInt32('vmaddr'),
                                                       UInt32('vmsize'),
                                                       UInt32('fileoff'),
                                                       UInt32('filesize'),
                                                       UInt32('maxprot'),
                                                       UInt32('initprot'),
                                                       UInt32('nsects'),
                                                       UInt32('flags'),
                                                       Rename("sections",
                                                              Array(lambda ctx: ctx['nsects'],
                                                                    Struct('Section',
                                                                           PaddedStringAdapter(Bytes('sectname', 16)),
                                                                           PaddedStringAdapter(Bytes('segname', 16)),
                                                                           UInt32('addr'),
                                                                           UInt32('size'),
                                                                           UInt32('offset'),
                                                                           UInt32('align'),
                                                                           UInt32('reloff'),
                                                                           UInt32('nreloc'),
                                                                           UInt32('flags'),
                                                                           UInt32('reserved1'),
                                                                           UInt32('reserved2'),
                                                                           ))),
                                                       ),
                                  'LC_SEGMENT_64': Segment64,
                                  'LC_DYLIB_CODE_SIGN_DRS': Struct("codesign_drs",
                                                                   UInt32('dataoff'),
                                                                   UInt32('datasize'),
                                                                   Pointer(lambda ctx: ctx['_']['_']['macho_start'] + ctx['dataoff'], Blob),
                                                                   ),
                                  'LC_CODE_SIGNATURE': Struct("codesig",
                                                              UInt32('dataoff'),
                                                              UInt32('datasize'),
                                                              Pointer(lambda ctx: ctx['_']['_']['macho_start'] + ctx['dataoff'], Blob),
                                                              ),
                                  }, default=Pass)),
                     OnDemand(Bytes('bytes', lambda ctx: ctx['cmdsize'] - 8)),
                     #Probe(),
                     )

MachO = Struct("MachO",
               Anchor("macho_start"),
               Enum(UInt32("magic"),
                    MH_MAGIC=0xfeedface,
                    MH_MAGIC_64=0xfeedfacf,
                    ),
               UInt32("cputype"),
               UInt32("cpusubtype"),
               Enum(UInt32("filetype"),
                    MH_OBJECT=0x1,
                    MH_EXECUTE=0x2,
                    MH_FVMLIB=0x3,
                    MH_CORE=0x4,
                    MH_PRELOAD=0x5,
                    MH_DYLIB=0x6,
                    MH_DYLINKER=0x7,
                    MH_BUNDLE=0x8,
                    MH_DYLIB_STUB=0x9,
                    MH_DSYM=0xa,
                    MH_KEXT_BUNDLE=0xb,
                    _default_=Pass,
                    ),
               UInt32("ncmds"),
               UInt32("sizeofcmds"),
               FlagsEnum(UInt32("flags"),
                         MH_NOUNDEFS=0x1,
                         MH_INCRLINK=0x2,
                         MH_DYLDLINK=0x4,
                         MH_BINDATLOAD=0x8,
                         MH_PREBOUND=0x10,
                         MH_SPLIT_SEGS=0x20,
                         MH_LAZY_INIT=0x40,
                         MH_TWOLEVEL=0x80,
                         MH_FORCE_FLAT=0x100,
                         MH_NOMULTIDEFS=0x200,
                         MH_NOFIXPREBINDING=0x400,
                         MH_PREBINDABLE=0x800,
                         MH_ALLMODSBOUND=0x1000,
                         MH_SUBSECTIONS_VIA_SYMBOLS=0x2000,
                         MH_CANONICAL=0x4000,
                         MH_WEAK_DEFINES=0x8000,
                         MH_BINDS_TO_WEAK=0x10000,
                         MH_ALLOW_STACK_EXECUTION=0x20000,
                         MH_ROOT_SAFE=0x40000,
                         MH_SETUID_SAFE=0x80000,
                         MH_NO_REEXPORTED_DYLIBS=0x100000,
                         MH_PIE=0x200000,
                         MH_DEAD_STRIPPABLE_DYLIB=0x400000,
                         MH_HAS_TLV_DESCRIPTORS=0x00800000,
                         MH_NO_HEAP_EXECUTION=0x01000000,
                         MH_APP_EXTENSION_SAFE=0x02000000,
                         MH_UNUSED_1=0x04000000,
                         MH_UNUSED_2=0x08000000,
                         MH_UNUSED_3=0x10000000,
                         MH_UNUSED_4=0x20000000,
                         MH_UNUSED_5=0x40000000,
                         MH_UNUSED_6=0x80000000,
                         ),
               If(lambda ctx: ctx['magic'] == 'MH_MAGIC_64', UInt32('reserved')), Rename('commands', Array(lambda ctx: ctx['ncmds'], LoadCommand)))

FatArch = Struct("FatArch",
                 UBInt32("cputype"),
                 UBInt32("cpusubtype"),
                 UBInt32("offset"),
                 UBInt32("size"),
                 UBInt32("align"),
                 Pointer(lambda ctx: ctx['offset'], MachO),
                 )

Fat = Struct("Fat",
             Const(UBInt32("magic"), 0xcafebabe),
             UBInt32("nfat_arch"),
             Array(lambda ctx: ctx['nfat_arch'], FatArch),
             )

MachoFile = Struct("MachoFile",
                   Peek(UInt32("magic")),
                   Switch("data", lambda ctx: ctx['magic'], {0xfeedface: MachO,
                                                             0xfeedfacf: MachO,
                                                             0xcafebabe: Fat,
                                                             0xbebafeca: Fat,
                                                             0xc10cdefa: Blob,
                                                             })
                   )
