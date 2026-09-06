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
    CodeInverseBoolMap,
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


class ChannelMute(CodeInverseBoolMap):
    """
    Speaker channel mute (CMU command). Wire "0" = muted, "1" = unmuted --
    CodeInverseBoolMap gives a natural is_muted semantic (True = muted).
    """

    friendly_name = "channel mute"
    base_property = "channel_mute"
    property_name = "mute"  # unused for decode -- see SpeakerChannelMute
    supported_zones = {Zone.Z1}  # only confirmed live against Main Zone so far


class SpeakerChannelMute(CodeMapSequence):
    """
    Speaker channel mute / test-tone toggle (CMU command).

    Used by the reference app during level calibration to temporarily silence or
    play a test tone per channel, but confirmed live to work as a genuine
    persistent per-channel mute independent of that context (state holds until
    explicitly toggled back).

    Confirmed via real app traffic capture (2026-09-06):
      - SET wire format: "<channel><0|1>CMU" (value-first, command-last -- same
        convention as ILV/CLV sends), e.g. "L__0CMU" = mute front left.
      - Responses are command-first as usual: "CMU<channel><0|1>".
      - QUERY is "?CMU<channel>" (command-first, channel as suffix) -- see the
        CodeMapBlank(0) prefix trick on the query_command registration below,
        same technique used for ILV's SET direction.
    """

    friendly_name = "speaker channel mute"
    base_property = "channel_mute"
    code_map_sequence = [SpeakerChannel, ChannelMute]

    @classmethod
    def decode_response(cls, response: Response, params: AVRParams) -> list[Response]:
        responses = super().decode_response(response=response, params=params)
        speaker = responses[0].value
        muted = responses[1].value
        response.update(code=responses[1].code, property_name=speaker, value=muted)
        return [response]


class ChannelLevelAt(ChannelLevel):
    """
    Channel level value at a fixed position within a bulk multi-channel level
    response/command (see SpeakerChannelLevelBulk). Same encoding as ChannelLevel
    (code 50 = 0dB, +/-1 = +/-0.5dB) -- only property_name differs per position.
    """

    def __new__(cls, channel: str):
        """Create a subclass bound to a fixed channel key."""
        return type(
            f"ChannelLevelAt_{channel}",
            (ChannelLevelAt,),
            {"friendly_name": f"channel level {channel}", "property_name": channel},
        )


class SpeakerChannelLevelBulk(CodeMapSequence):
    """
    Speaker channel level, bulk multi-channel variant (ILV command).

    Used by AVRs (FY11-FY14 generation, e.g. VSX-924/VSX-1021) that report/accept
    ALL channel levels in a single fixed-width message instead of the per-channel
    CLV/ZGE/ZHE command family. Field order and scaling were reverse engineered
    from the iControlAV2014 Android app
    (jp.pioneer.avsoft.android.icontrolav.memory.remocon.avr.status.h / .j) and
    confirmed against a real VSX-924: each field is 2 digits, code 50 = 0dB,
    +/-1 = +/-0.5dB -- identical encoding to ChannelLevel/CLV, just packed
    positionally with no channel-code prefix.

    Wire format for SET, confirmed live against a real VSX-924 (differs from
    both the naive "ILV"+data guess AND from what the decompiled app's own
    aq.java/ar.java SET methods do):
      - the full 20-field sequence must be sent, not just the base 12 -- the
        receiver rejects a 12-field SET as "unknown command" even though the
        decompiled app itself never sends more than 12. Whatever the app's own
        historical limitation was, this receiver's firmware accepts (and
        requires) the complete sequence.
      - the command name goes at the END of the message ("<20 fields>ILV"), not
        the start -- matching this receiver's convention for other small
        prefix-style commands too (e.g. CLV set command wire format is
        confirmed to be "<channel><level>CLV", and CMU send order was
        independently captured as value-then-command as well). The QUERY
        direction is the opposite: "?ILV" out, "ILV<data>" back.
      - SW (index 7, the legacy single-subwoofer field) and SW1 (index 18) are
        NOT mirrors of each other on this receiver, contrary to what the
        decompiled app's "plain model" branch of h.a(float) suggested --
        setting index 7 alone, confirmed live, did not change index 18's
        reported value. They are mapped to distinct properties accordingly.
    """

    friendly_name = "speaker channel level (bulk)"
    base_property = "channel_level"
    property_name = "bulk"  # unused for actual storage -- see ChannelLevelAt

    ## Base 12 channels -- present on all generations that support ILV.
    code_map_sequence = [
        ChannelLevelAt("L"),
        ChannelLevelAt("R"),
        ChannelLevelAt("C"),
        ChannelLevelAt("SL"),
        ChannelLevelAt("SR"),
        ChannelLevelAt("SBL"),
        ChannelLevelAt("SBR"),
        ChannelLevelAt("SW"),
        ChannelLevelAt("FHL"),
        ChannelLevelAt("FHR"),
        ChannelLevelAt("FWL"),
        ChannelLevelAt("FWR"),
    ]
    ## FY13+ AVRs extend the response with top/height channels and an
    ## independent SW1/SW2 stereo-subwoofer level (empirically NOT the same as
    ## the legacy SW field at index 7 -- see class docstring). Two further
    ## fields reported by the source app after this (RearHeightL/R) are always
    ## a verbatim mirror of TRL/TRR on receivers without dedicated Top Rear
    ## speakers -- intentionally not exposed separately here since they never
    ## carry independent information.
    code_map_sequence_extra_1 = [
        *code_map_sequence,
        ChannelLevelAt("TML"),
        ChannelLevelAt("TMR"),
        ChannelLevelAt("TFL"),
        ChannelLevelAt("TFR"),
        ChannelLevelAt("TRL"),
        ChannelLevelAt("TRR"),
        ChannelLevelAt("SW1"),
        ChannelLevelAt("SW2"),
    ]

    @classmethod
    def _sequence_for_length(cls, code_len: int) -> list:
        if code_len >= cls.get_len_sequence(cls.code_map_sequence_extra_1):
            return cls.code_map_sequence_extra_1
        return cls.code_map_sequence

    @classmethod
    def decode_response(cls, response: Response, params: AVRParams) -> list[Response]:
        return cls.decode_response_sequence(
            response=response,
            params=params,
            code_map_sequence=cls._sequence_for_length(len(response.code)),
        )

    @classmethod
    def get_nargs(cls) -> int:
        ## parse_args below takes (channel, level), not one arg per sequence field
        return 2

    @classmethod
    def get_parser(cls, parser) -> None:
        SpeakerChannel.get_parser(parser)
        ChannelLevel.get_parser(parser)

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
        Build a full ILV SET string (all 20 fields -- see class docstring) by
        merging the requested channel/level change into the most recently known
        levels for the other channels. The AVR requires the whole sequence sent
        together in one message; there is no per-channel set variant.
        """
        cls.check_args(args)
        channel, level = args
        sequence = cls.code_map_sequence_extra_1
        settable_channels = [c.property_name for c in sequence]
        if channel not in settable_channels:
            raise ValueError(
                f"channel {channel!r} cannot be set via the bulk speaker level "
                f"command (known channels: {settable_channels})"
            )
        current = dict(properties.channel_level.get(zone, {}))
        current[channel] = level
        return "".join(
            ChannelLevel.value_to_code(current.get(c.property_name, 0))
            for c in sequence
        )


class GraphicEqBand(CodeFloatMap):
    """
    Graphic EQ band level (ATB command). Same (code - 50) * 0.5 dB scale as
    ChannelLevel/ILV/CLV -- see GraphicEqBulk docstring for how this was confirmed.
    """

    friendly_name = "graphic EQ band level"
    base_property = "graphic_eq"
    property_name = "band"  # unused for decode -- see GraphicEqBandAt

    value_min = -12
    value_max = 12
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

    Confirmed via real app traffic capture (2026-09-06) -- see PROTOCOL_FINDINGS.md
    for the full session log. Two earlier code-derived guesses (`AEQ`, then `ACE`,
    traced from the decompiled `gl.java`/`FingerEqStatus`/`EmphasisViewFingerEQ`
    classes) were both rejected live by the receiver as "unknown command" -- `ATB`
    was only found by capturing the official app's own traffic, not from the code.

    Wire format: 11 fields of 2 chars each (22 chars total), same (code - 50) * 0.5
    dB scale as ChannelLevel/ILV/CLV:
      - field[0]: constant "00" throughout the capture -- unidentified (possibly a
        zone or response-type flag), not exposed as a property.
      - fields[1..9]: the 9 bands, confirmed in order by watching the user adjust
        them "low to high" in the app and observing each field lock in one at a
        time: 63Hz, 125Hz, 250Hz, 500Hz, 1kHz, 2kHz, 4kHz, 8kHz, 16kHz.
      - field[10]: untouched throughout the capture (stayed at code 50 / 0dB) --
        possibly a global "all bands" level mirroring `FingerEqStatus.level_All`
        in the decompiled app (which the ACE/AEQ encoder explicitly excluded from
        its 9-band array). Decoded here for completeness; meaning not confirmed.

    Query-only for now: `?ATB` out, `ATB<data>` back is confirmed, and the receiver
    echoes `ATB<data>` back unchanged for every band the app touched in the capture
    -- but that capture never isolated a genuine outbound SET frame from the
    response echo, so it's still unknown whether SET follows the value-first,
    command-last convention used by ILV/CLV/CMU or is command-first like the
    response. Do not add a set_command here without a capture that confirms it.
    """

    friendly_name = "graphic equalizer"
    base_property = "graphic_eq"
    property_name = "bulk"  # unused for actual storage -- see GraphicEqBandAt

    code_map_sequence = [
        CodeMapBlank(2),  # field[0]: constant "00", unidentified
        GraphicEqBandAt("63HZ"),
        GraphicEqBandAt("125HZ"),
        GraphicEqBandAt("250HZ"),
        GraphicEqBandAt("500HZ"),
        GraphicEqBandAt("1KHZ"),
        GraphicEqBandAt("2KHZ"),
        GraphicEqBandAt("4KHZ"),
        GraphicEqBandAt("8KHZ"),
        GraphicEqBandAt("16KHZ"),
        GraphicEqBandAt("ALL"),  # field[10]: untouched in capture, meaning unconfirmed
    ]


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
    ## Bulk-format equivalent of the above for FY11-FY14 AVRs (e.g. VSX-924) that
    ## do not support CLV/ZGE/ZHE -- see SpeakerChannelLevelBulk docstring.
    ## NOTE: SET wire format is confirmed live to be "<data>ILV" (command name
    ## LAST), the reverse of the QUERY direction ("?ILV" out, "ILV<data>" back)
    ## -- matching how CLV's own SET is confirmed to send "<channel><level>CLV".
    ## Since send_command's generic single-avr_arg path already places the
    ## encoded args as a *prefix* before avr_command (see property_entry.py /
    ## pioneer_avr.py send_command), the default single-item avr_args=[code_map]
    ## from gen_set_property already produces exactly "<data>" + "ILV" -- no
    ## override needed here (unlike an earlier, incorrect attempt at this).
    gen_set_property(
        SpeakerChannelLevelBulk,
        {Zone.Z1: "ILV"},
        query_command=AVRCommand(is_query_command=True, wait_for_response=True),
    ),
    ## Per-channel mute / test-tone toggle, confirmed live via real app traffic
    ## capture (see SpeakerChannelMute docstring). SET uses the default
    ## prefix behaviour (channel+value before "CMU", same as ILV/CLV). QUERY
    ## is "?CMU<channel>" (command first) -- CodeMapBlank(0) forces the channel
    ## arg into the suffix slot so it lands after "?CMU" instead of before it.
    gen_set_property(
        SpeakerChannelMute,
        {Zone.Z1: "CMU"},
        query_command=AVRCommand(
            avr_commands={Zone.Z1: "?CMU"},
            avr_args=[CodeMapBlank(0), SpeakerChannel],
            wait_for_response=True,
        ),
    ),
    ## 9-band graphic EQ, confirmed live via real app traffic capture (see
    ## GraphicEqBulk docstring). Query-only -- SET wire format not yet confirmed
    ## from a genuine SET capture, do not add a set_command without one. Command
    ## explicitly named "query_audio_..." (rather than the "query_graphic_eq_bulk"
    ## gen_query_property would derive from base_property/property_name) so it
    ## falls under the existing "audio" PARAM_ENABLED_FUNCTIONS bucket and gets
    ## auto-refreshed like other audio properties, without adding a new bucket
    ## just for this one feature.
    gen_query_property(
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
