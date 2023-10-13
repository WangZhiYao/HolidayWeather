from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix='HOLIDAY_WEATHER',
    settings_files=['settings.toml', '.secrets.toml'],
    validators=[
        Validator("provider.weather", must_exist=True),
        Validator("provider.push", must_exist=True),
        Validator("qweather.range", must_exist=True, when=Validator("provider.weather", eq="qweather")),
        Validator("colorful_clouds.range", must_exist=True,
                  when=Validator("provider.weather", eq="colorful_clouds")),
        Validator("smtp.host", "smtp.port", "smtp.sender", "smtp.password", must_exist=True,
                  when=Validator("provider.push", eq="smtp"))
    ]
)
