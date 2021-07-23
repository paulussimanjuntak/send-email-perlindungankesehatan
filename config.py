from phonenumbers import (
    NumberParseException,
    PhoneNumberType,
    PhoneNumberFormat,
    format_number,
    number_type,
    is_valid_number,
    parse as parse_phone_number
)
from pydantic import BaseSettings, BaseModel, constr, validator
from fastapi.templating import Jinja2Templates

class Settings(BaseSettings):
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_tls: bool

    email_receiver: str

class SendEmailSchema(BaseModel):
    name: constr(strict=True, max_length=100)
    phone: constr(strict=True, max_length=20)
    message: constr(strict=True)

    @validator('phone')
    def validate_no_wa(cls, v):
        try:
            n = parse_phone_number(v, None)
        except NumberParseException as e:
            raise ValueError('Please provide a valid mobile phone number') from e

        MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            raise ValueError('Please provide a valid mobile phone number')

        return format_number(n, PhoneNumberFormat.INTERNATIONAL)

    class Config:
        min_anystr_length = 3
        anystr_strip_whitespace = True


settings = Settings()
templates = Jinja2Templates(directory="templates")
