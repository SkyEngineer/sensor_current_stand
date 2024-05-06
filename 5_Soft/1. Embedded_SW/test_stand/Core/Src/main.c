/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "usb_device.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "usbd_cdc_if.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
struct point
{
    unsigned char x:7;   // 0-7
};

// для разбиения по битам
union code
{
    struct point p;
    struct{
        unsigned a0:1;
        unsigned a1:1;
        unsigned a2:1;
        unsigned a3:1;
        unsigned a4:1;
        unsigned a5:1;
        unsigned a6:1;
        unsigned a7:1;
    } byte;
};
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
// ответ на запрос
uint8_t ID[1]={0xBB};

// ответ на команду включения, что мы не зависли и отвечаем
uint8_t ANTWORT[1]={0xEE};
uint8_t ANTWORT_DT[1]={0xCC};
// входной буфер
uint8_t RxData[1] = {0};

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */
void Init_MUX(void);
void Reset_all_addr_MUX(void);
void Reset_all_addr_MUX_and_U_MUX(void);

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
// инициализация выходов мультиплексоров
void Init_MUX(void)
{
	// сначала адресные выходы в ноль
	Reset_all_addr_MUX();

	// подаем питание
	HAL_GPIO_WritePin(E_U_MUX_GPIO_Port, E_U_MUX_Pin, GPIO_PIN_SET);

	// задержку на переходный процесс
	HAL_Delay(100);
}

// отключение адресных выходов для всех мультиплексоров
void Reset_all_addr_MUX(void)
{
	// сначал запрет общий для всх групп, потом адреса обнуляем
	HAL_GPIO_WritePin(MUX_1_E_GPIO_Port, MUX_1_E_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(MUX_2_E_GPIO_Port, MUX_2_E_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(MUX_3_E_GPIO_Port, MUX_3_E_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(MUX_4_E_GPIO_Port, MUX_4_E_Pin, GPIO_PIN_RESET);

	// Группа 1. Адреса
	HAL_GPIO_WritePin(MUX_1_S0_GPIO_Port, MUX_1_S0_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(MUX_1_S1_GPIO_Port, MUX_1_S1_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(MUX_1_S2_GPIO_Port, MUX_1_S2_Pin, GPIO_PIN_RESET);

	// Группа 2. Адреса
	HAL_GPIO_WritePin(MUX_2_S0_GPIO_Port, MUX_2_S0_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(MUX_2_S1_GPIO_Port, MUX_2_S1_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(MUX_2_S2_GPIO_Port, MUX_2_S2_Pin, GPIO_PIN_RESET);

	// Группа 3. Адреса
	HAL_GPIO_WritePin(MUX_3_S0_GPIO_Port, MUX_3_S0_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(MUX_3_S1_GPIO_Port, MUX_3_S1_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(MUX_3_S2_GPIO_Port, MUX_3_S2_Pin, GPIO_PIN_RESET);

	// Группа 4. Адреса
	HAL_GPIO_WritePin(MUX_4_S0_GPIO_Port, MUX_4_S0_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(MUX_4_S1_GPIO_Port, MUX_4_S1_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(MUX_4_S2_GPIO_Port, MUX_4_S2_Pin, GPIO_PIN_RESET);

}

void Reset_all_addr_MUX_and_U_MUX(void)
{
	Reset_all_addr_MUX();
	HAL_GPIO_WritePin(E_U_MUX_GPIO_Port, E_U_MUX_Pin, GPIO_PIN_RESET);
}

void Enable_Sensor_Current(uint8_t num)
{
	// отключаем все адресные выходы
	Reset_all_addr_MUX();

	/* включаем мультиплексор нужной группы----------------*/
	// Группа 1 0x01...0x8 (1...8)
	if ((num >= 0x01) && (num <= 0x08))
	{
		HAL_GPIO_WritePin(MUX_1_E_GPIO_Port, MUX_1_E_Pin, GPIO_PIN_SET);
		// включаем определенный датчик
		struct point center = {num-1};
		union code c;
		c.p = center;

		HAL_GPIO_WritePin(MUX_1_S0_GPIO_Port, MUX_1_S0_Pin, c.byte.a0);
		HAL_GPIO_WritePin(MUX_1_S1_GPIO_Port, MUX_1_S1_Pin, c.byte.a1);
		HAL_GPIO_WritePin(MUX_1_S2_GPIO_Port, MUX_1_S2_Pin, c.byte.a2);
	}
	// Группа 2 0x09...0x10 (9...16)
	if ((num >= 0x09) && (num <= 0x10))
	{
		HAL_GPIO_WritePin(MUX_2_E_GPIO_Port, MUX_2_E_Pin, GPIO_PIN_SET);
		struct point center = {num-1-8};
		union code c;
		c.p = center;

		HAL_GPIO_WritePin(MUX_2_S0_GPIO_Port, MUX_2_S0_Pin, c.byte.a0);
		HAL_GPIO_WritePin(MUX_2_S1_GPIO_Port, MUX_2_S1_Pin, c.byte.a1);
		HAL_GPIO_WritePin(MUX_2_S2_GPIO_Port, MUX_2_S2_Pin, c.byte.a2);
	}

	// Группа 3 0x11...0x18 (17...24)
	if ((num >= 0x11) && (num <= 0x18))
	{
		HAL_GPIO_WritePin(MUX_3_E_GPIO_Port, MUX_3_E_Pin, GPIO_PIN_SET);
		struct point center = {num-1-24};
		union code c;
		c.p = center;

		HAL_GPIO_WritePin(MUX_3_S0_GPIO_Port, MUX_3_S0_Pin, c.byte.a0);
		HAL_GPIO_WritePin(MUX_3_S1_GPIO_Port, MUX_3_S1_Pin, c.byte.a1);
		HAL_GPIO_WritePin(MUX_3_S2_GPIO_Port, MUX_3_S2_Pin, c.byte.a2);
	}

	// Группа 4 0x19...0x20 (25...32)
	if ((num >= 0x19) && (num <= 0x20))
	{
		HAL_GPIO_WritePin(MUX_4_E_GPIO_Port, MUX_4_E_Pin, GPIO_PIN_SET);
		struct point center = {num-1-31};
		union code c;
		c.p = center;

		HAL_GPIO_WritePin(MUX_4_S0_GPIO_Port, MUX_4_S0_Pin, c.byte.a0);
		HAL_GPIO_WritePin(MUX_4_S1_GPIO_Port, MUX_4_S1_Pin, c.byte.a1);
		HAL_GPIO_WritePin(MUX_4_S2_GPIO_Port, MUX_4_S2_Pin, c.byte.a2);
	}
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USB_DEVICE_Init();
  /* USER CODE BEGIN 2 */

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  // инициализируем выходы и подаем питание
  Init_MUX();

  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

	  	  //обработка запроса
	  	  CDC_Receive_FS(RxData,  (uint32_t)1);

	  	  // тут мы смотрим что пришло (всего 255 команд может прийти)
	  	  // 1. в зависимости от того какое число - включаем определенный мультиплексор
	  	  // 2. Если числа с 1(0x01) до 32 (0x20) - это номер датчика для включения (свободными остаются еще 223)
	  	  // 3. Если число 0xAA - это запрос опознания, отвечаем на это 0xBB
	  	  // 4. Если число 0xFE - это команда полной остановки работы мультиплексора (без отключения питания)
	  	  // 5. Если число 0xFF - это команда полной остановки работы мультиплексора (с отключением питания)

	  	  // необходимо отработать условие, что одновременно может быть включен только один датчик
	  	  // то есть каждый раз обнуляем все выходы
	  	  //

	  	  // если у нас присланный запрос - в диапазоне номеров датчиков
	  	  if ((RxData[0] > 0x00) && (RxData[0] <= 0x20))
	  	  {
	  		  Enable_Sensor_Current(RxData[0]);
	  		  RxData[0] = 0;
	  		  // передаём ответ
	  		  CDC_Transmit_FS(ANTWORT_DT, 1);								// отвечаем, что выставили пин
	  	  }
	  	  // если нет
	  	  else
	  	  {
	  		  switch (RxData[0])
	  		  {
	  			case 0xAA: //запрос опознания, отвечаем на это 0xBB
	  				CDC_Transmit_FS(ID, 1);
	  				RxData[0] = 0;
	  				break;
	  			case 0xFE:
	  				// отключение адресных выходов для всех мультиплексоров
	  				Reset_all_addr_MUX();
	  				RxData[0] = 0;
	  				CDC_Transmit_FS(ANTWORT, 1);
	  				break;
	  			case 0xFF: //команда полной остановки работы мультиплексора (с отключением питания мультиплексоров)
	  				Reset_all_addr_MUX_and_U_MUX();
	  				CDC_Transmit_FS(ANTWORT, 1);
	  				RxData[0] = 0;
	  				break;

	  			default:
	  				//CDC_Transmit_FS(0x00, 1);
	  				break;

	  		  }
	  	  }
	  	  HAL_Delay(10);

	  /*

	  HAL_Delay(100);
	  HAL_GPIO_TogglePin(E_U_MUX_GPIO_Port, E_U_MUX_Pin);
	  CDC_Receive_FS(RxData,  (uint32_t)1);
	  CDC_Transmit_FS(ANTWORT, 1);*/

  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE3);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 7;
  RCC_OscInitStruct.PLL.PLLN = 72;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 3;
  RCC_OscInitStruct.PLL.PLLR = 2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
