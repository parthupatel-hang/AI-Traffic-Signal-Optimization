"""Fixed-cycle and adaptive traffic-signal controller."""

class TrafficLightController:
    ROADS = ("N", "E", "S", "W")

    def __init__(self):
        self.MIN_GREEN = 8
        self.MAX_GREEN = 30
        self.YELLOW_TIME = 3
        self.ALL_RED_TIME = 2
        self.EARLY_SWITCH_THRESHOLD = 8
        self.EMERGENCY_BONUS = 1000
        self.current_green = "N"
        self.phase_mode = "GREEN"
        self.phase = "N_GREEN"
        self.green_elapsed = self.yellow_elapsed = self.all_red_elapsed = 0.0
        self.pending_green = None
        self.last_reason = "INIT"
        self.states = {road: ("GREEN" if road == "N" else "RED") for road in self.ROADS}

    def get_states(self): return self.states.copy()
    def get_phase(self): return self.phase
    def get_current_green_direction(self): return self.current_green
    def get_remaining_green_seconds(self):
        if self.phase_mode == "GREEN": return max(0, int(round(self.MAX_GREEN - self.green_elapsed)))
        if self.phase_mode == "YELLOW": return max(0, int(round(self.YELLOW_TIME - self.yellow_elapsed)))
        return max(0, int(round(self.ALL_RED_TIME - self.all_red_elapsed)))
    def get_last_reason(self): return self.last_reason

    def _set_green(self, direction):
        self.states = {road: "RED" for road in self.ROADS}; self.states[direction] = "GREEN"
        self.current_green = direction; self.phase_mode = "GREEN"; self.phase = f"{direction}_GREEN"
        self.green_elapsed = self.yellow_elapsed = self.all_red_elapsed = 0.0

    def _set_yellow(self):
        self.states = {road: "RED" for road in self.ROADS}; self.states[self.current_green] = "YELLOW"
        self.phase_mode = "YELLOW"; self.phase = f"{self.current_green}_YELLOW"; self.yellow_elapsed = 0.0

    def _set_all_red(self):
        self.states = {road: "RED" for road in self.ROADS}; self.phase_mode = "ALL_RED"; self.phase = "ALL_RED"; self.all_red_elapsed = 0.0

    def _next_round_robin(self):
        return self.ROADS[(self.ROADS.index(self.current_green) + 1) % len(self.ROADS)]

    def _scores(self, density, waiting, predicted_direction=None, emergency_dir=None):
        return {road: density.get(road, 0) * 5 + waiting.get(road, 0.0) * 2 + (6 if road == predicted_direction else 0) + (self.EMERGENCY_BONUS if road == emergency_dir else 0) for road in self.ROADS}

    def _transition_after_clearance(self):
        self._set_green(self.pending_green or self._next_round_robin()); self.pending_green = None

    def automatic_cycle(self, dt_ms=30):
        dt = dt_ms / 1000.0
        if self.phase_mode == "GREEN":
            self.green_elapsed += dt
            if self.green_elapsed >= self.MAX_GREEN:
                self.pending_green = self._next_round_robin(); self.last_reason = "FIXED_MAX_GREEN"; self._set_yellow()
        elif self.phase_mode == "YELLOW":
            self.yellow_elapsed += dt
            if self.yellow_elapsed >= self.YELLOW_TIME: self._set_all_red()
        else:
            self.all_red_elapsed += dt
            if self.all_red_elapsed >= self.ALL_RED_TIME: self._transition_after_clearance()

    def ai_control(self, density, waiting, predicted_direction=None, emergency_flag=False, emergency_dir=None, dt_ms=30):
        dt = dt_ms / 1000.0
        if self.phase_mode == "GREEN":
            self.green_elapsed += dt
            scores = self._scores(density, waiting, predicted_direction, emergency_dir if emergency_flag else None)
            best, current = max(scores, key=scores.get), self.current_green
            if self.green_elapsed >= self.MAX_GREEN:
                self.pending_green = best; self.last_reason = f"MAX_GREEN_TO_{best}"; self._set_yellow(); return
            if self.green_elapsed < self.MIN_GREEN: return
            if emergency_flag and emergency_dir and emergency_dir != current:
                self.pending_green = emergency_dir; self.last_reason = f"EMERGENCY_TO_{emergency_dir}"; self._set_yellow(); return
            if best != current and scores[best] >= scores[current] + self.EARLY_SWITCH_THRESHOLD:
                self.pending_green = best; self.last_reason = f"HIGHER_PRIORITY_TO_{best}"; self._set_yellow()
        elif self.phase_mode == "YELLOW":
            self.yellow_elapsed += dt
            if self.yellow_elapsed >= self.YELLOW_TIME: self._set_all_red()
        else:
            self.all_red_elapsed += dt
            if self.all_red_elapsed >= self.ALL_RED_TIME: self._transition_after_clearance()
