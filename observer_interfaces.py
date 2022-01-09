from __future__ import annotations

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject) -> None:
        pass


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass

    @abstractmethod
    def print_x_report(self) -> None:
        pass

    @abstractmethod
    def close_cashier(self) -> None:
        pass
