"""aiopioneer response decoders for audio responses."""

from ..command_queue import CommandItem
from ..const import Zone
from ..exceptions import AVRCommandUnavailableError
from ..params import AVRParams
from ..properties import AVRProperties
from ..property_entry import AVRCommand, gen_query_property, gen_set_property
from .code_map import (
    CodeDefault,
    CodeMapBlank,
    CodeMapSequence,
    CodeMapQuery,
    CodeDynamicDictStrMap,
    CodeDynamicDictListMap,
    CodeDictStrMap,
    CodeStrMap,
    CodeBoolMap,
    CodeIntMap,
    CodeFloatMap,
)
from .response import Response


class AudioChannelActive(CodeDictStrMap):
    """Audio channel active."""

    friendly_name = "audio channel active"
    base_property = "audio"
    property_name = "channel_active"  # unused

    code_map = {
        "0": "inactive",
        "1": "active",
    }

    def __new__(cls, channel_type: str, channel: str):
        """Create a subclass for channel type and name."""
        return type(
            f"AudioChannelActive_{channel_type}_{channel}",
            (AudioChannelActive,),
            {
                "friendly_name": f"{channel_type} channel {channel}",
                "property_name": f"{channel_type}_channels.{channel}",
            },
        )


class AudioInputMultichannel(CodeBoolMap):
    """Audio input multichannel."""

    friendly_name = "audio input multichannel"
    base_property = "audio"
    property_name = "input_multichannel"

    @classmethod
    def decode_response(
        cls,
        response: Response,
        params: AVRParams,
    ) -> list[Response]:
        """Response decoder for input multichannel."""

        def check_input_multichannel(response: Response) -> list[Response]:
            """Trigger listening mode update if input multichannel has changed."""
            if response.properties.audio.get("input_multichannel") == response.value:
                return []
            response.update(
                queue_commands=[CommandItem("_update_listening_modes", queue_id=3)]
            )
            return [response]

        super().decode_response(response=response, params=params)
        response.update(callback=check_input_multichannel)
        return [response]

    @classmethod
    def code_to_value(cls, code: str) -> bool:
        return all([CodeBoolMap[c] for c in code])


class AudioSignalInputInfo(CodeDictStrMap):
    """Audio signal input info."""

    friendly_name = "audio input signal"  # NOTE: inconsistent
    base_property = "audio"
    property_name = "input_signal"

    code_map = {
        "00": "ANALOG",
        "01": "ANALOG",
        "02": "ANALOG",
        "03": "PCM",
        "04": "PCM",
        "05": "DOLBY DIGITAL",
        "06": "DTS",
        "07": "DTS-ES Matrix",
        "08": "DTS-ES Discrete",
        "09": "DTS 96/24",
        "10": "DTS 96/24 ES Matrix",
        "11": "DTS 96/24 ES Discrete",
        "12": "MPEG-2 AAC",
        "13": "WMA9 Pro",
        "14": "DSD (HDMI or File via DSP route)",
        "15": "HDMI THROUGH",
        "16": "DOLBY DIGITAL PLUS",
        "17": "DOLBY TrueHD",
        "18": "DTS EXPRESS",
        "19": "DTS-HD Master Audio",
        "20": "DTS-HD High Resolution",
        "21": "DTS-HD High Resolution",
        "22": "DTS-HD High Resolution",
        "23": "DTS-HD High Resolution",
        "24": "DTS-HD High Resolution",
        "25": "DTS-HD High Resolution",
        "26": "DTS-HD High Resolution",
        "27": "DTS-HD Master Audio",
        "28": "DSD (HDMI or File via DSD DIRECT route)",
        "29": "Dolby Atmos",
        "30": "Dolby Atmos over Dolby Digital Plus",
        "31": "Dolby Atmos over Dolby TrueHD",
        "64": "MP3",
        "65": "WAV",
        "66": "WMA",
        "67": "MPEG4-AAC",
        "68": "FLAC",
        "69": "ALAC(Apple Lossless)",
        "70": "AIFF",
        "71": "DSD (USB-DAC)",
        "72": "Spotify",
    }


class AudioSignalFrequency(CodeDictStrMap):
    """Audio signal frequency."""

    friendly_name = "audio frequency"
    base_property = "audio"
    property_name = "frequency"  # unused

    code_map = {
        CodeDefault(): None,
        "00": "32kHz",
        "01": "44.1kHz",
        "02": "48kHz",
        "03": "88.2kHz",
        "04": "96kHz",
        "05": "176.4kHz",
        "06": "192kHz",
        # "07": "---",
        "32": "2.8MHz",
        "33": "5.6MHz",
    }


class AudioInputFrequency(AudioSignalFrequency):
    """Audio input frequency."""

    friendly_name = "audio input frequency"
    base_property = "audio"
    property_name = "input_frequency"


class AudioOutputFrequency(AudioSignalFrequency):
    """Audio output frequency."""

    friendly_name = "audio output frequency"
    base_property = "audio"
    property_name = "output_frequency"


class AudioOutputBits(CodeIntMap):
    """Audio output bits."""

    friendly_name = "audio output bits"
    base_property = "audio"
    property_name = "output_bits"

    code_zfill = 2


class AudioOutputPqls(CodeDictStrMap):
    """Audio output PQLS."""

    friendly_name = "audio output PQLS"
    base_property = "audio"
    property_name = "output_pqls"

    code_map = {"0": "off", "1": "2h", "2": "Multi-channel", "3": "Bitstream"}


class AudioOutputAutoPhaseControlPlus(CodeIntMap):
    """Audio output auto phase control plus."""

    friendly_name = "audio output auto phase control plus"
    base_property = "audio"
    property_name = "output_auto_phase_control_plus"

    code_zfill = 2


class AudioOutputReversePhase(CodeBoolMap):
    """Audio output reverse phase."""

    friendly_name = "audio output reverse phase"
    base_property = "audio"
    property_name = "output_reverse_phase"


class AudioInformation(CodeMapSequence):
    """Audio information."""

    friendly_name = "audio information"
    base_property = "audio"
    property_name = "information"  # unused

    code_map_sequence = [
        AudioSignalInputInfo,  # [0:2] audio.input_signal
        AudioInputFrequency,  # [2:4] audio.input_frequency
        AudioChannelActive("input", "L"),  # [4]
        AudioChannelActive("input", "C"),  # [5]
        AudioChannelActive("input", "R"),  # [6]
        AudioChannelActive("input", "SL"),  # [7]
        AudioChannelActive("input", "SR"),  # [8]
        AudioChannelActive("input", "SBL"),  # [9]
        AudioChannelActive("input", "SBC"),  # [10]
        AudioChannelActive("input", "SBR"),  # [11]
        AudioChannelActive("input", "LFE"),  # [12]
        AudioChannelActive("input", "FHL"),  # [13]
        AudioChannelActive("input", "FHR"),  # [14]
        AudioChannelActive("input", "FWL"),  # [15]
        AudioChannelActive("input", "FWR"),  # [16]
        AudioChannelActive("input", "XL"),  # [17]
        AudioChannelActive("input", "XC"),  # [18]
        AudioChannelActive("input", "XR"),  # [19]
        CodeMapBlank(5),  ## (data21) to (data25) are reserved according to FY16AVRs
        AudioChannelActive("output", "L"),  # [25]
        AudioChannelActive("output", "C"),  # [26]
        AudioChannelActive("output", "R"),  # [27]
        AudioChannelActive("output", "SL"),  # [28]
        AudioChannelActive("output", "SR"),  # [29]
        AudioChannelActive("output", "SBL"),  # [30]
        AudioChannelActive("output", "SBC"),  # [31]
        AudioChannelActive("output", "SBR"),  # [32]
    ]
    code_map_sequence_extra_1 = [
        *code_map_sequence,
        AudioChannelActive("output", "SW"),  # [33]
        AudioChannelActive("output", "FHL"),  # [34]
        AudioChannelActive("output", "FHR"),  # [35]
        AudioChannelActive("output", "FWL"),  # [36]
        AudioChannelActive("output", "FWR"),  # [37]
        AudioChannelActive("output", "TML"),  # [38]
        AudioChannelActive("output", "TMR"),  # [39]
        AudioChannelActive("output", "TRL"),  # [40]
        AudioChannelActive("output", "TRR"),  # [41]
        AudioChannelActive("output", "SW2"),  # [42]
    ]
    code_map_sequence_extra_2 = [
        *code_map_sequence_extra_1,
        AudioOutputFrequency,  # [43:45] audio.output_frequency
        AudioOutputBits,  # [45:47] audio.output_bits
        CodeMapBlank(4),
        AudioOutputPqls,  # [51] audio.output_pqls
        AudioOutputAutoPhaseControlPlus,  # [52:54] audio.output_auto_phase_control_plus
        AudioOutputReversePhase,  # [54] audio.output_reverse_phase
    ]

    @classmethod
    def decode_response(
        cls,
        response: Response,
        params: AVRParams,
    ) -> list[Response]:
        """Response decoder for audio information."""
        code_map_sequence = cls.code_map_sequence

        if len(response.code) >= 55:
            code_map_sequence = cls.code_map_sequence_extra_2
        elif len(response.code) >= 43:
            ## FY11 AVRs do not have more than 43 data bits (VSX-1021)
            code_map_sequence = cls.code_map_sequence_extra_1

        responses = AudioInputMultichannel.decode_response(
            response=response.clone(code=response.code[4:7]), params=params
        )
        responses.extend(
            cls.decode_response_sequence(
                response=response, params=params, code_map_sequence=code_map_sequence
            )
        )
        return responses


class ChannelLevel(CodeFloatMap):
    """Channel level (1step = 0.5dB)."""

    friendly_name = "channel level"
    base_property = "channel_level"
    property_name = "level"  # unused for decode

    value_min = -12
    value_max = 12
    value_step = 0.5
    value_divider = 0.5
    value_offset = 25
    code_zfill = 2
    icon = "mdi:tune-vertical-variant"
    supported_zones = {Zone.Z1, Zone.Z2, Zone.Z3}
    unit_of_measurement = "dB"
    ha_auto_entity = False
    ha_enable_default = True
    ha_device_class = "signal_strength"
    ha_number_mode = "slider"


class SpeakerChannel(CodeStrMap):
    """Speaker channel."""

    friendly_name = "speaker channel"
    base_property = "channel_level"
    property_name = "channel"  # unused for decode
    code_len = 3

    CHANNELS_ALL = {
        "L": "front left",
        "C": "center",
        "R": "front right",
        "SL": "surround left",
        "SR": "surround right",
        "SBL": "surround back left",
        "SBC": "surround back center",
        "SBR": "surround back right",
        "LFE": "low freqeuency effects",
        "FHL": "front height left",
        "FHR": "front height right",
        "FWL": "front wide left",
        "FWR": "front wide right",
        "TML": "top middle left",
        "TMR": "top middle right",
        "TFL": "top forward left",  # NOTE: not in AudioInformation
        "TFR": "top forward right",  # NOTE: not in AudioInformation
        "TRL": "top backward left",
        "TRR": "top backward right",
        "SW": "subwoofer",
        "SW2": "subwoofer 2",
    }

    @classmethod
    def value_to_code(cls, value: str) -> str:
        if value == "all":
            value = value.upper()
        elif value not in cls.CHANNELS_ALL:
            raise ValueError(f"unknown channel {value} for {cls.get_name()}")
        return super().value_to_code(value=value)

    @classmethod
    def code_to_value(cls, code: str) -> str:
        return super().code_to_value(code=code).upper()

    @classmethod
    def parse_args(
        cls,
        command: str,
        args: list,
        zone: Zone,
        params: AVRParams,
        properties: AVRProperties,
    ) -> str:
        channel: str = args[0]
        if channel != "all" and zone in properties.zones_initial_refresh:
            if (channel_levels := properties.channel_level.get(zone)) is None:
                raise AVRCommandUnavailableError(
                    command=command, err_key="channel_level", zone=zone
                )
            if channel_levels.get(channel) is None:
                raise AVRCommandUnavailableError(
                    command=command, err_key="channel", zone=zone, channel=channel
                )
        return super().parse_args(
            command=command, args=args, zone=zone, params=params, properties=properties
        )


class SpeakerChannelLevel(CodeMapSequence):
    """Speaker channel level."""

    friendly_name = "speaker channel level"
    base_property = "channel_level"
    code_map_sequence = [SpeakerChannel, ChannelLevel]

    @classmethod
    def decode_response(cls, response: Response, params: AVRParams) -> list[Response]:
        responses = super().decode_response(response=response, params=params)
        speaker = responses[0].value
        level = responses[1].value
        level_code = responses[1].code
        if speaker == "ALL":
            responses = []
            channel_levels = response.properties.channel_level.get(response.zone, {})
            for channel in channel_levels.keys():
                responses.append(
                    response.clone(code=level_code, property_name=channel, value=level)
                )
            return responses
        response.update(code=level_code, property_name=speaker, value=level)
        return [response]


class GraphicEqBand(CodeFloatMap):
    """
    Graphic EQ band level (ATB command). Same (code - 50) * 0.5 dB scale as
    ChannelLevel/ILV/CLV -- see GraphicEqBulk docstring for how this was confirmed.
    Range is +/-6dB (code 38-62), confirmed live by driving all 9 bands to both
    slider extremes (2026-09-06) -- narrower than ChannelLevel/ILV's +/-12dB.
    """

    friendly_name = "graphic EQ band level"
    base_property = "graphic_eq"
    property_name = "level"  # unused for decode -- see GraphicEqBandAt

    value_min = -6
    value_max = 6
    value_step = 0.5
    value_divider = 0.5
    value_offset = 25
    code_zfill = 2
    icon = "mdi:equalizer"
    supported_zones = {Zone.Z1}  # only confirmed live against Main Zone so far
    unit_of_measurement = "dB"
    ha_auto_entity = False
    ha_enable_default = True
    ha_number_mode = "slider"


class GraphicEqBandAt(GraphicEqBand):
    """Graphic EQ band value at a fixed position within the ATB bulk response."""

    def __new__(cls, band: str):
        """Create a subclass bound to a fixed band key."""
        return type(
            f"GraphicEqBandAt_{band}",
            (GraphicEqBandAt,),
            {"friendly_name": f"graphic EQ band {band}", "property_name": band},
        )


class GraphicEqBulk(CodeMapSequence):
    """
    9-band graphic equalizer, bulk multi-band variant (ATB command).

    Confirmed via two real app traffic captures (2026-09-06) -- see
    PROTOCOL_FINDINGS.md for the full session log. Two earlier code-derived guesses
    (`AEQ`, then `ACE`, traced from the decompiled `gl.java`/`FingerEqStatus`/
    `EmphasisViewFingerEQ` classes) were both rejected live by the receiver as
    "unknown command" -- `ATB` was only found by capturing the official app's own
    traffic, not from the code.

    Wire format: 11 fields of 2 chars each (22 chars total), same (code - 50) * 0.5
    dB scale as ChannelLevel/ILV/CLV:
      - field[0]: constant "00" throughout both captures -- unidentified (possibly
        a zone or response-type flag), not exposed as a property.
      - fields[1..9]: the 9 bands, confirmed in order twice -- once by watching the
        user adjust them "low to high" and observing each field lock in one at a
        time, and again by driving every band to both slider extremes one at a
        time: 63Hz, 125Hz, 250Hz, 500Hz, 1kHz, 2kHz, 4kHz, 8kHz, 16kHz. Confirmed
        range is code 38-62 (+/-6dB) -- every band hit exactly 38 at max-negative
        and 62 at max-positive, consistently.
      - field[10]: untouched throughout both captures (stayed at code 50 / 0dB) --
        possibly a global "all bands" level mirroring `FingerEqStatus.level_All`
        in the decompiled app (which the ACE/AEQ encoder explicitly excluded from
        its 9-band array). Decoded here for completeness; meaning still unconfirmed,
        not exposed as settable.

    SET confirmed live (2026-09-06, second capture): value-first, command-last --
    `"<22-char-data>ATB"` -- the exact same convention as ILV/CLV/CMU. The app's
    in-EQ "Reset" button sends the identical SET format with every band back at
    code 50, not a separate command. Since send_command's generic single-avr_arg
    path already places the encoded args as a prefix before avr_command, the
    default single-item avr_args=[code_map] from gen_set_property already produces
    exactly "<data>" + "ATB" -- no override needed (same reasoning as ILV).
    """

    friendly_name = "graphic equalizer"
    base_property = "graphic_eq"
    property_name = "bulk"  # unused for actual storage -- see GraphicEqBandAt

    ## The 9 bands actually exposed/settable via the app's graphic EQ UI, confirmed
    ## live. Does NOT include "ALL" (field[10]) -- that field was never touched in
    ## either capture and its meaning/settability is unconfirmed, so it's decoded
    ## for visibility but deliberately excluded from what callers can set.
    BANDS = [
        "63HZ", "125HZ", "250HZ", "500HZ", "1KHZ", "2KHZ", "4KHZ", "8KHZ", "16KHZ",
    ]

    code_map_sequence = [
        CodeMapBlank(2),  # field[0]: constant "00", unidentified
        *(GraphicEqBandAt(band) for band in BANDS),
        GraphicEqBandAt("ALL"),  # field[10]: untouched in both captures, meaning unconfirmed
    ]

    @classmethod
    def get_nargs(cls) -> int:
        ## parse_args below takes (band, level), not one arg per sequence field
        return 2

    @classmethod
    def get_parser(cls, parser) -> None:
        parser.add_argument("band", choices=cls.BANDS, help="graphic EQ band")
        GraphicEqBand.get_parser(parser)

    @classmethod
    def parse_args(
        cls,
        command: str,  # pylint: disable=unused-argument
        args: list,
        zone: Zone,
        params: AVRParams,  # pylint: disable=unused-argument
        properties: AVRProperties,
    ) -> str:
        """
        Build a full 11-field ATB SET string by merging the requested band/level
        change into the most recently known levels for the other bands -- the AVR
        requires the whole sequence sent together in one message, same as ILV.
        """
        cls.check_args(args)
        band, level = args
        if band not in cls.BANDS:
            raise ValueError(
                f"band {band!r} cannot be set via the graphic EQ bulk command "
                f"(known bands: {cls.BANDS})"
            )
        current = dict(properties.graphic_eq.get(zone, {}))
        current[band] = level
        return "00" + "".join(
            GraphicEqBand.value_to_code(current.get(c.property_name, 0))
            for c in cls.code_map_sequence
            if issubclass(c, GraphicEqBand)
        )


class ListeningModeIndex(CodeIntMap):
    """Listening mode index."""

    friendly_name = "listening mode"

    value_min = 0
    value_max = 9999
    code_zfill = 4


class ListeningMode(CodeDynamicDictListMap):
    """Listening mode."""

    friendly_name = "listening mode"
    base_property = "listening_mode"

    index_map_class = ListeningModeIndex

    @classmethod
    def value_to_code(cls, value: str, properties: AVRProperties = None) -> str:
        if not isinstance(properties, AVRProperties):
            raise RuntimeError(f"AVRProperties required for {cls.get_name()}")
        return cls.value_to_code_dynamic(value, code_map=properties.listening_modes_all)

    @classmethod
    def code_to_value(cls, code: str, properties: AVRProperties = None) -> str:
        if not isinstance(properties, AVRProperties):
            raise RuntimeError(f"AVRProperties required for {cls.get_name()}")
        return cls.code_to_value_dynamic(code, code_map=properties.listening_modes_all)

    @classmethod
    def parse_args(
        cls,
        command: str,  # pylint: disable=unused-argument
        args: list,
        zone: Zone,  # pylint: disable=unused-argument
        params: AVRParams,  # pylint: disable=unused-argument
        properties: AVRProperties,
    ) -> str:
        return cls.parse_args_dynamic(
            command=command,
            args=args,
            zone=zone,
            params=params,
            properties=properties,
            code_map=properties.listening_modes_all,
        )

    @classmethod
    def decode_response(
        cls,
        response: Response,
        params: AVRParams,
    ) -> list[Response]:
        """Response decoder for listening mode."""
        cls.decode_response_dynamic(
            response=response,
            params=params,
            code_map=response.properties.listening_modes_all,
        )
        return [
            response,
            response.clone(
                base_property="listening_mode_id",
                value=cls.index_map_class.code_to_value(code=response.code),
            ),
        ]


# pylint: disable=abstract-method
class AvailableListeningMode(CodeDynamicDictStrMap):  # encode only
    """Available listening mode."""

    index_map_class = ListeningModeIndex
    base_property = "listening_mode"

    @classmethod
    def value_to_code(cls, value: str | int, properties: AVRProperties = None) -> str:
        if not isinstance(properties, AVRProperties):
            raise RuntimeError(f"AVRProperties required for {cls.get_name()}")
        if isinstance(value, int):
            return cls.index_map_class.value_to_code(value=value)
        return cls.value_to_code_dynamic(
            value, code_map=properties.available_listening_modes
        )

    @classmethod
    def parse_args(
        cls,
        command: str,
        args: list,
        zone: Zone,  # pylint: disable=unused-argument
        params: AVRParams,  # pylint: disable=unused-argument
        properties: AVRProperties,
    ) -> str:
        return cls.parse_args_dynamic(
            command=command,
            args=args,
            zone=zone,
            params=params,
            properties=properties,
            code_map=properties.available_listening_modes,
        )

    ## NOTE: code_to_value unimplemented


class ToneMode(CodeDictStrMap):
    """Tone mode."""

    friendly_name = "tone mode"
    base_property = "tone"
    property_name = "status"
    supported_zones = {Zone.Z1, Zone.Z2}
    icon = "mdi:music-box-outline"
    ha_enable_default = True

    code_map = {"0": "bypass", "1": "on"}


class ToneDb(CodeIntMap):
    """Tone dB value."""

    value_min = -6
    value_max = 6
    value_divider = -1
    value_offset = -6
    code_zfill = 2
    supported_zones = {Zone.Z1, Zone.Z2}
    unit_of_measurement = "dB"
    ha_auto_entity = False
    ha_enable_default = True
    ha_device_class = "signal_strength"
    ha_number_mode = "slider"


class ToneBass(ToneDb):
    """Tone bass."""

    friendly_name = "tone bass"
    base_property = "tone"
    property_name = "bass"
    icon = "mdi:music-clef-bass"


class ToneTreble(ToneDb):
    """Tone treble."""

    friendly_name = "tone treble"
    base_property = "tone"
    property_name = "treble"
    icon = "mdi:music-clef-treble"


PROPERTIES_AUDIO = [
    gen_query_property(AudioInformation, {Zone.ALL: "AST"}, query_group="basic"),
    gen_set_property(
        SpeakerChannelLevel,
        {Zone.Z1: "CLV", Zone.Z2: "ZGE", Zone.Z3: "ZHE"},
        query_command=AVRCommand(
            avr_args=[CodeMapQuery(SpeakerChannel)],
            wait_for_response=True,
        ),
    ),
    ## 9-band graphic EQ, confirmed live via two real app traffic captures (see
    ## GraphicEqBulk docstring) -- both decode AND set_command are now confirmed.
    ## Query command explicitly named "query_audio_..." (rather than the
    ## "query_graphic_eq_bulk" gen_query_property would derive from
    ## base_property/property_name) so it falls under the existing "audio"
    ## PARAM_ENABLED_FUNCTIONS bucket and gets auto-refreshed like other audio
    ## properties, without adding a new bucket just for this one feature.
    gen_set_property(
        GraphicEqBulk,
        {Zone.Z1: "ATB"},
        query_command=AVRCommand(
            name="query_audio_graphic_eq", is_query_command=True, wait_for_response=True
        ),
    ),
    gen_set_property(
        ListeningMode,
        {Zone.ALL: "SR"},
        query_command=AVRCommand(avr_commands={Zone.Z1: ["?S", "SR"]}),
        set_command=AVRCommand(
            name="select_listening_mode",
            avr_args=[AvailableListeningMode],
            wait_for_response=True,
            retry_on_fail=True,
        ),
    ),
    gen_set_property(
        ToneMode,
        {Zone.Z1: "TO", Zone.Z2: "ZGA"},
        query_command="query_tone_status",
        set_command="set_tone_mode",
        retry_set_on_fail=True,
    ),
    gen_set_property(ToneBass, {Zone.Z1: "BA", Zone.Z2: "ZGB"}),
    gen_set_property(ToneTreble, {Zone.Z1: "TR", Zone.Z2: "ZGC"}),
]
