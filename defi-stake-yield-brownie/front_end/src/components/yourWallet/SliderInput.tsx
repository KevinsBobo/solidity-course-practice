import { Input, makeStyles, Slider, Theme, Typography } from "@material-ui/core";


export interface SliderInputProps {
    lable?: string
    id?: string
    maxValue: number
    value: number | string | (string | number)[]
    onChange: (newValue: number | string | Array<number | string>) => void
    disabled?: boolean
    [x: string]: any
}

const useStyles = makeStyles((theme: Theme) => ({
    inputsContainer: {
        display: "grid",
        gap: theme.spacing(3),
        gridTemplateRows: "auto",
        gridTemplateColumns: "1fr auto",
    },
}));


function valuetext(value: number) {
    return `${value}%`
}

export const SliderInput = ({
    label = "",
    id = "input-slider",
    maxValue,
    value,
    onChange,
    disabled = false,
    ...rest
}: SliderInputProps) => {
    const classes = useStyles()

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        let newValue: any = event.target.value === "" ? "" : Number(event.target.value)
        onChange(newValue)
        // console.log(newValue)
    }
    const handleSliderChange = (event: any, newValue: number | number[]) => {
        onChange(newValue)
    };


    const handleBlur = () => {
        if (value === "") {
            onChange(0)
        }
        else if (value < 0) {
            onChange(0)
        } else if (value > maxValue) {
            onChange(maxValue)
        }
    };
    const sliderMarks = [
        {
            value: 0,
            label: "0%",
        },
        {
            value: maxValue,
            label: "100%",
        },
    ]

    const sliderStep = maxValue / 100;
    const inputStep = maxValue / 50;

    return (
        <div {...rest}>
            {label && (<Typography id={id} gutterBottom>
                {label}
            </Typography>
            )}
            <div className={classes.inputsContainer}>
                <div>
                    <Slider
                        value={typeof value === 'number' ? value : 0}
                        onChange={handleSliderChange}
                        aria-labelledby={id}
                        max={maxValue}
                        getAriaValueText={valuetext}
                        // valueLabelDisplay="auto"
                        disabled={disabled}
                        step={sliderStep}
                        marks={disabled ? [] : sliderMarks}
                    />
                </div>
                <div>
                    <Input
                        value={value}
                        margin="dense"
                        onChange={handleInputChange}
                        onBlur={handleBlur}
                        inputProps={{
                            step: inputStep,
                            min: 0,
                            max: maxValue,
                            type: 'number',
                            'aria-labelledby': id,
                        }}
                    />
                </div>
            </div>
        </div>
    )
}