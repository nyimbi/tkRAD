#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    TkRAD - Tkinter Rapid Application Development

    (c) 2013 Raphaël SEBAN <motus@laposte.net>

    released under Creative Commons BY-SA 3.0

    see http://creativecommons.org/licenses/by-sa/3.0/
"""



# lib imports

import tkinter as TK

from ..core import tools

from . import rad_frame as RF



class RADStatusBar (RF.RADFrame):
    r"""
        generic status bar for rapid application development (RAD);

        supports direct and constant display of message;

        e.g. self.info("Ready.");

        supports notification-type message (short-living message);

        e.g. self.notify("This message will end in 5 seconds.");

        supports notification delay settings;

        e.g. self.delay = 5.2  # in seconds;
    """



    NOTIFICATION_DELAY = 5                                  # in seconds



    def _stop_notification (self):
        r"""
            protected method def;

            stops any pending notification and

            resets process id pointer;

            no return value (void);
        """

        # stop any pending notification

        self.after_cancel(self.__notify_pid)

        # reset process id

        self.__notify_pid = 0

    # end def



    @property
    def delay (self):
        r"""
            returns current internal notification delay value;
        """

        return self.__delay

    # end def



    @delay.setter
    def delay (self, value):

        self.__delay = max(0.5, tools.ensure_float(value))

    # end def



    @delay.deleter
    def delay (self):

        del self.__delay

    # end def



    def get_correct_delay (self, value = None):
        r"""
            tries to retrieve a correct delay value amongst many;

            returns found value or at least 0.5, otherwise;
        """

        return max(

            0.5,

            tools.choose_num(

                lambda x: x >= 0,

                value,

                self.options["gui"].get("statusbar_notification_delay"),

                self.delay,

                self.NOTIFICATION_DELAY,

                5                                   # last but not least
            )
        )

    # end def



    def info(self, text = None):
        r"""
            sets the highest priority-level message for this status

            bar object;

            any pending notifications will be stopped to ensure the

            current message won't be masked at any time;

            no return value (void);
        """

        # stop any pending notification

        self._stop_notification()

        # default text inits

        self.__static_text = tools.choose_str(

            text,

            self.__static_text,

            _("Ready."),

            "Ready."                                # last but not least
        )

        # end if

        self.message.set(self.__static_text)

    # end def



    def init_widget (self, **kw):
        r"""
            inherited method from RADWidgetBase base class;

            here come the main inits;

            no return value (void);
        """

        # member inits

        self.__notify_pid = 0

        self.__static_text = None

        self.__toggle_var = None

        self.delay = self.NOTIFICATION_DELAY

        # rc options inits

        self.options.set_sections("gui")

        self.options.load()

        # widget inits

        self.message = TK.StringVar()

        self.label = TK.Label(

            self,

            textvariable = self.message,

            anchor = TK.W,

            justify = TK.LEFT,

            relief = TK.SUNKEN,
        )

        self.label.pack(padx = 2, pady = 2, **self.PACK_OPTIONS)

        self.info()

    # end def



    def notify (self, text, delay = None):
        r"""
            sets a low priority-level message for a delayed bit of

            time (in seconds);

            any pending notifications will be stopped to ensure the

            current message won't be masked at any time;

            no return value (void);
        """

        # param controls

        if tools.is_pstr(text):

            # stop any pending notification

            self._stop_notification()

            # set new message

            self.message.set(text)

            # look for a correct value

            delay = self.get_correct_delay(delay)

            # restore static text after @delay (in seconds)

            # notice: @delay param can be of 'int' or 'float' type /!\

            self.__notify_pid = self.after(

                tools.ensure_int(delay * 1000.0),

                self.info
            )

        # end if

    # end def



    def toggle (self, *args, **kw):
        r"""
            switches ON / OFF display of status bar along toggle_var

            internal integer value (0 = OFF, other = ON);

            raises "StatusbarShow" and "StatusbarHide" named events

            just before toggling display of status bar;

            these events are of tkRAD.core.events type, *NOT* of

            tkinter ones;

            /!\ notice: for technical reasons, toggling is only done

            with self.grid() and self.grid_remove() methods

            as self.pack() and self.pack_forget() do *NOT* keep

            correctly the reserved space for status bar in window;

            no return value (void);
        """

        # tk control var inits

        _value = self.toggle_var.get()

        # update config options

        self.options["gui"]["show_statusbar"] = str(_value)

        # show status bar

        if tools.ensure_int(_value):

            self.events.raise_event("StatusbarShow", widget = self)

            self.grid()

        # hide status bar

        else:

            self.events.raise_event("StatusbarHide", widget = self)

            self.grid_remove()

        # end if

    # end def



    @property
    def toggle_var (self):
        r"""
            returns current internal tkinter StringVar control variable;
        """

        return self.__toggle_var

    # end def



    @toggle_var.setter
    def toggle_var (self, arg):

        # param control

        if isinstance(arg, TK.StringVar):

            self.__toggle_var = arg

        else:

            raise TypeError(
                _(
                    "Statusbar toggle variable must be "

                    "of type {obj_type}."

                ).format(obj_type = repr(TK.StringVar))
            )

            # set a rescue var nevertheless

            self.__toggle_var = TK.StringVar()

        # end if

        # config options inits

        self.__toggle_var.set(

            self.options["gui"].get("show_statusbar", "1")
        )

    # end def



    @toggle_var.deleter
    def toggle_var (self):

        del self.__toggle_var

    # end def


# end class RADStatusBar
