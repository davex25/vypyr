import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

from threading import Timer

import mido
import time

class Application(object):
    def __init__(self, *args, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.midi_out = None
        self._create_main_window()
        self.Tempo = 120
        self.sendTempoChange();

    def onDeleteWindow(self, *args):
        print("quitting")
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("quitting")
        Gtk.main_quit()

    def onTempoActivated(self, entry):
        entry.set_text("")

    def onTempoEntered(self, entry):
        print("Entered text ", entry.get_text())
        try:
            tempo = int(entry.get_text())
            if tempo < 20:
                self.Tempo = 20
            elif tempo > 300:
                entry.set_text("300")
                self.Tempo = 300
            else:
                self.Tempo = tempo
                self.sendTempoChange()
                print("valid tempo set")
        except ValueError:
            entry.set_text("")

    def onPlayNote(self, button):
        outputNames = mido.get_output_names()
        name = next((outN for outN in outputNames if "Synth input port" in outN), None)
        if name != None:
            print("Note played")
            output = mido.open_output(name)
            output.send(mido.Message('note_on', note=60, velocity=64))
        else:
            print("No output device")

    def _create_main_window(self):
        builder = Gtk.Builder()
        builder.add_from_file("vypyr/main_dialog.ui")
        builder.connect_signals(self)
        self.tempo = builder.get_object("txtTempo")
        self.window = builder.get_object("main_window")

    def print_message(message):
        print(message)

    def setup_midi_in(self):
        print("setting up midi input")
        inputNames = mido.get_input_names()
        vypyrInput = next((name for name in inputNames if 'VYPYR USB Interface MIDI' in name), None)
        if vypyrInput != None:
            self.midi_in = mido.open_input(vypyrInput)

    def setup_vypyrOut(self):
        print("Setting up midi output")
        outputNames = mido.get_output_names()
        print(outputNames)
        vypyrOutput = next((name for name in outputNames if 'VYPYR USB Interface MIDI' in name), None)
        if vypyrOutput != None:
            self.midi_out = mido.open_output(vypyrOutput)
            return True

        return False

    def poll_midi_input(self):
        try:
            #print("polling midi input")
            for msg in self.midi_in.iter_pending():
                print(msg)
        except Exception as e:
            print("Exception encountered")
            print(e)

        finally:
            GLib.idle_add(self.poll_midi_input)


    def send_tap_tempo(self):
        if self.midi_out == None:
            return

        message = mido.Message('note_on', note=0x0B, velocity=127, time=20)
        self.midi_out.send(message)

    def sendTempoChange(self):
        if self.midi_out == None:
            if not self.setup_vypyrOut():
                print("Unable to detect VYPYR midi device")
                return

        delaytime = 500
        delayMSB = (delaytime & 0xF80) >> 8
        delayLSB = (delaytime & 0x7F)
        print("delaytime=" + str(delayMSB) + ", " + str(delayLSB))
        message = mido.Message('control_change', channel=0, control=0x58, value=delayMSB)
        self.midi_out.send(message)
        message = mido.Message('control_change', channel=0, control=0x59, value=delayLSB)
        self.midi_out.send(message)
        message = mido.Message('control_change', channel=0, control=0x5B, value=127)
        self.midi_out.send(message)
        message = mido.Message('control_change', channel=0, control=16, value=127)
        self.midi_out.send(message)
        message = mido.Message('control_change', channel=0, control=17, value=64)
        self.midi_out.send(message)
        message = mido.Message('control_change', channel=0, control=18, value=50)
        self.midi_out.send(message)
        message = mido.Message('control_change', channel=0, control=19, value=85)
        self.midi_out.send(message)
        message = mido.Message('control_change', channel=0, control=20, value=10)
        self.midi_out.send(message)
        self.send_tap_tempo()

        Timer(.5, self.send_tap_tempo, ()).start()

    def run(self):
        print(self.window)
        self.setup_midi_in()
        self.window.show_all()
        print("Showing window")

        if hasattr(self, 'midi_in'):
            GLib.idle_add(self.poll_midi_input)

        Gtk.main()
